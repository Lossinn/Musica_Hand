"""Armazón de la aplicación: contenedor de servicios, ventana y navegación."""

from __future__ import annotations

import logging
import sys
import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from .core.config import APP_NAME, APP_VERSION, Settings, settings as load_settings
from .core.events import BUS
from .data.database import Database, get_db, set_db
from .data.repositories import (AchievementRepository, ActivityRepository,
                                AttemptRepository, ProfileRepository,
                                ResultRepository, RewardRepository,
                                SessionRepository, SkillRepository,
                                SkillStateRepository)
from .data.seed import seed
from .domain.entities import LearningSession, Profile
from .intelligence.optimizer import SessionOptimizer
from .intelligence.predictor import MasteryPredictor
from .learning.adaptation import AdaptationEngine
from .music.audio import AudioEngine
from .music.engine import MusicEngine
from .ui import theme as T
from .vision.service import GestureService

log = logging.getLogger(__name__)

# Pantallas donde la cámara evalúa gestos en tiempo real: ahí el único sonido
# que debe competir por la atención del niño es el de la propia nota, así que
# la música de fondo se apaga. En el resto ("pantallas principales": mapa,
# inicio, progreso, ajustes, catálogo de canciones, resultados...) suena en
# bucle. La pantalla de bienvenida se excluye de esta lista aparte: administra
# su propia música ("musica_inicio") en vez de la de fondo.
PANTALLAS_SIN_MUSICA_DE_FONDO = frozenset(
    {"calibration", "exercise", "freeplay", "rhythm"})


class AppContext:
    """Todo lo que las pantallas necesitan, en un solo objeto.

    Se pasa por constructor en lugar de usar variables globales, de modo que las
    pruebas pueden montar un contexto con una base de datos temporal.
    """

    def __init__(self, db: Database | None = None,
                 settings: Settings | None = None) -> None:
        self.settings = settings or load_settings()
        self.db = db or get_db()
        seed(self.db)

        self.profiles = ProfileRepository(self.db)
        self.skills = SkillRepository(self.db)
        self.skill_states = SkillStateRepository(self.db)
        self.activities = ActivityRepository(self.db)
        self.attempts = AttemptRepository(self.db)
        self.results = ResultRepository(self.db)
        self.sessions = SessionRepository(self.db)
        self.rewards = RewardRepository(self.db)
        self.achievements = AchievementRepository(self.db)

        self.audio = AudioEngine(self.settings.audio)
        self.music = MusicEngine(self.audio)
        self.gestures = GestureService(self.settings)
        self.adaptation = AdaptationEngine(
            mastery_threshold=self.settings.learning.mastery_threshold)
        self.optimizer = SessionOptimizer(
            budget_minutes=self.settings.learning.session_minutes,
            session_size=self.settings.learning.activities_per_session,
            prefer_milp=self.settings.learning.use_milp)
        # Arranca sin entrenar; select_profile() carga el modelo propio de
        # cada niño (uno por perfil, guardado en `meta`) si ya existe.
        self.predictor = MasteryPredictor()

        self.profile: Profile | None = None
        self.session: LearningSession | None = None
        self.bus = BUS
        # Memoria de la sesión, para el motor adaptativo.
        self.session_results: list = []
        self.consecutive_failures = 0
        self.last_optimizer_method = ""

    # ------------------------------------------------------------- perfil
    def select_profile(self, profile: Profile) -> None:
        self.profile = self.profiles.touch(profile)
        if not self.skill_states.for_profile(profile.id):
            self.skill_states.initialize(profile.id, self.skills.all())
        self.gestures.set_profile(profile.id)
        self.session = self.sessions.start(profile.id)
        self.session_results = []
        self.consecutive_failures = 0
        self.profile.calibrated = self.gestures.calibrated
        self.profiles.save(self.profile)
        # Cada niño tiene su propio Agente Adaptativo: se carga lo que ya se
        # entrenó con SUS datos (nada se comparte entre perfiles).
        self.predictor = MasteryPredictor.from_json(
            self.db.get_meta(f"predictor_{profile.id}"))

    def save_predictor(self) -> None:
        if self.profile is not None:
            self.db.set_meta(f"predictor_{self.profile.id}",
                             self.predictor.to_json())

    def end_session(self) -> None:
        if self.session:
            precisiones = [r.accuracy for r in self.session_results]
            self.session.accuracy = (sum(precisiones) / len(precisiones)
                                     if precisiones else 0.0)
            self.session.activities_done = len(self.session_results)
            self.sessions.end(self.session)
            self.session = None

    @property
    def minutes_in_session(self) -> float:
        if not self.session:
            return 0.0
        return (time.time() - self.session.started_at) / 60.0

    def shutdown(self) -> None:
        try:
            self.gestures.stop()
        except Exception:
            pass
        self.end_session()
        self.settings.save()


def _app_icon() -> QIcon:
    """Icono generado al vuelo: una nota sobre un círculo amarillo."""
    pm = QPixmap(128, 128)
    pm.fill(QColor(0, 0, 0, 0))
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(T.C.sun))
    p.drawEllipse(4, 4, 120, 120)
    p.setPen(QColor("#3A2E00"))
    f = T.font(74, display=True)
    p.setFont(f)
    p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, "♪")
    p.end()
    return QIcon(pm)


class MainWindow(QMainWindow):
    def __init__(self, ctx: AppContext) -> None:
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.setWindowIcon(_app_icon())
        self.resize(1280, 820)
        self.setMinimumSize(1060, 700)

        self.stack = QStackedWidget()
        self.stack.setObjectName("RootSurface")
        self.setCentralWidget(self.stack)

        self._screens: dict[str, object] = {}
        self._build_screens()
        self.navigate("splash")

    # ---------------------------------------------------------- pantallas
    def _build_screens(self) -> None:
        from .ui.screens.adventure import AdventureScreen
        from .ui.screens.calibration import CalibrationScreen
        from .ui.screens.exercise import ExerciseScreen
        from .ui.screens.freeplay import FreePlayScreen
        from .ui.screens.home import HomeScreen
        from .ui.screens.parents import ParentsScreen
        from .ui.screens.profiles import CreateProfileScreen, ProfilesScreen
        from .ui.screens.progress import ProgressScreen
        from .ui.screens.results import ResultsScreen
        from .ui.screens.rhythm import RhythmScreen
        from .ui.screens.settings import SettingsScreen
        from .ui.screens.songs import SongsScreen
        from .ui.screens.splash import SplashScreen

        registro = {
            "splash": SplashScreen, "profiles": ProfilesScreen,
            "create_profile": CreateProfileScreen, "home": HomeScreen,
            "adventure": AdventureScreen, "calibration": CalibrationScreen,
            "exercise": ExerciseScreen, "results": ResultsScreen,
            "progress": ProgressScreen, "parents": ParentsScreen,
            "settings": SettingsScreen, "freeplay": FreePlayScreen,
            "songs": SongsScreen, "rhythm": RhythmScreen,
        }
        for nombre, klass in registro.items():
            pantalla = klass(self.ctx)
            pantalla.navigate.connect(self.navigate)
            self._screens[nombre] = pantalla
            self.stack.addWidget(pantalla)

    def navigate(self, name: str, kwargs: dict | None = None) -> None:
        kwargs = kwargs or {}
        actual = self.stack.currentWidget()
        destino = self._screens.get(name)
        if destino is None:
            log.warning("pantalla desconocida: %s", name)
            return
        if actual is not None and actual is not destino:
            try:
                actual.on_leave()
            except Exception:
                log.exception("fallo al salir de la pantalla")
        self.stack.setCurrentWidget(destino)
        try:
            destino.on_enter(**kwargs)
        except Exception:
            log.exception("fallo al entrar en la pantalla %s", name)
        self._actualizar_musica_de_fondo(name)

    def _actualizar_musica_de_fondo(self, name: str) -> None:
        """Mantiene la música de fondo fuera de las pantallas con cámara
        activa. La pantalla de bienvenida no se toca aquí: ella maneja su
        propia música de bienvenida al entrar y salir."""
        if name == "splash":
            return
        if name in PANTALLAS_SIN_MUSICA_DE_FONDO:
            self.ctx.audio.stop_music()
        else:
            self.ctx.audio.play_music("musica_fondo")

    def closeEvent(self, event) -> None:
        self.ctx.shutdown()
        super().closeEvent(event)


def run() -> int:
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s %(name)s: %(message)s")
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    T.load_bundled_fonts()
    app.setStyleSheet(T.global_stylesheet())

    ctx = AppContext()
    QTimer.singleShot(0, ctx.audio.preload)
    window = MainWindow(ctx)
    if ctx.settings.fullscreen:
        window.showFullScreen()
    else:
        window.show()
    return app.exec()
