from manim import *

class CyberAttackSimulation(Scene):
    def construct(self):
        # --- CONFIGURAZIONE VISIVA ---
        self.camera.background_color = "#1e1e1e" # Dark background

        # --- DEFINIZIONE NODI C1 (Difensore - Stella) ---
        # n1 è il centro (Database), gli altri sono satelliti
        c1_center = Dot(point=[2, 0, 0], radius=0.15, color=BLUE)
        c1_satellites = VGroup()
        c1_positions = [
            [2, 2, 0], [3.5, 0.5, 0], [3.5, -0.5, 0], [2, -2, 0]
        ]
        # Il nodo n3 (vulnerabile) lo posizioniamo verso sinistra, vicino agli attaccanti
        n3_pos = [0.5, 0, 0] 
        c1_n3 = Dot(point=n3_pos, radius=0.15, color=BLUE)
        
        for pos in c1_positions:
            c1_satellites.add(Dot(point=pos, radius=0.15, color=BLUE))

        c1_group = VGroup(c1_center, c1_satellites, c1_n3)
        
        # Etichette C1
        lbl_c1 = Text("C1: Target Infrastructure", font_size=20, color=BLUE).next_to(c1_center, UP, buff=2.5)
        lbl_n1 = Text("DB (n1)", font_size=14).next_to(c1_center, RIGHT)
        lbl_n3 = Text("Web (n3)", font_size=14).next_to(c1_n3, DOWN)

        # Archi C1 (Legittimi)
        edges_c1 = VGroup()
        for sat in c1_satellites:
            edges_c1.add(Line(c1_center.get_center(), sat.get_center(), stroke_width=2, color=BLUE_E))
        edge_n1_n3 = Line(c1_center.get_center(), c1_n3.get_center(), stroke_width=2, color=BLUE_E)
        edges_c1.add(edge_n1_n3)

        # --- DEFINIZIONE NODI C2 (Attaccante) ---
        c2_group = VGroup()
        c2_positions = [[-5, 1, 0], [-5, 0, 0], [-5, -1, 0]]
        for i, pos in enumerate(c2_positions):
            c2_group.add(Dot(point=pos, radius=0.15, color=RED))
        
        # Etichette C2
        lbl_c2 = Text("C2: Attacker", font_size=20, color=RED).next_to(c2_group, UP, buff=1)
        
        # --- ANIMAZIONE 1: SETUP ---
        self.play(FadeIn(lbl_c1), FadeIn(lbl_c2))
        self.play(
            LaggedStart(
                Create(c1_group), Create(edges_c1), Create(c2_group),
                Write(lbl_n1), Write(lbl_n3),
                lag_ratio=0.1
            )
        )
        self.wait(1)

        # --- ANIMAZIONE 2: ATTACCO E INFILTRAZIONE (WebShell) ---
        attack_arrow = Arrow(start=[-5, 0, 0], end=n3_pos, color=RED, buff=0.2)
        alert_text_1 = Text("Phase 1: Infiltration (WebShell)", font_size=24, color=RED).to_edge(UP)
        
        self.play(Write(alert_text_1))
        self.play(GrowArrow(attack_arrow))
        self.play(Flash(c1_n3, color=RED, flash_radius=0.5))
        
        # Cambio colore n3 (compromesso)
        self.play(c1_n3.animate.set_color(ORANGE))
        self.wait(1)

        # --- ANIMAZIONE 3: MOVIMENTO LATERALE ---
        lat_mov_arrow = CurvedArrow(n3_pos, [2, 0, 0], angle=-TAU/4, color=ORANGE)
        alert_text_2 = Text("Phase 2: Lateral Movement to DB", font_size=24, color=ORANGE).to_edge(UP)
        
        self.play(Transform(alert_text_1, alert_text_2))
        self.play(Create(lat_mov_arrow))
        self.play(c1_center.animate.set_color(ORANGE)) # DB Compromesso
        self.wait(1)

        # --- ANIMAZIONE 4: RILEVAZIONE ENTROPIA ---
        # Simuliamo un grafo dell'entropia che schizza in alto
        axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 10, 5], 
            x_length=2, y_length=1.5,
            axis_config={"include_tip": False}
        ).to_corner(DR)
        
        graph_label = Text("Entropy E(t)", font_size=18).next_to(axes, UP)
        curve = axes.plot(lambda x: 0.5 if x < 2.5 else 8, color=YELLOW) # Salto entropico
        
        self.play(Create(axes), Write(graph_label))
        self.play(Create(curve, run_time=2))
        
        alert_box = Rectangle(width=4, height=1, color=RED, fill_opacity=0.8).move_to([0, 2.5, 0])
        alert_msg = Text("ANOMALY DETECTED!", font_size=30, weight=BOLD).move_to(alert_box)
        
        self.play(FadeIn(alert_box), Write(alert_msg))
        self.wait(1)

        # --- ANIMAZIONE 5: PLAYBOOK RESPONSE (Contenimento) ---
        resp_text = Text("Phase 3: Playbook Containment", font_size=24, color=GREEN).to_edge(UP)
        
        self.play(Transform(alert_text_1, resp_text))
        self.play(FadeOut(alert_box), FadeOut(alert_msg))
        
        # Taglio delle connessioni
        self.play(
            Uncreate(attack_arrow),
            Uncreate(lat_mov_arrow),
            c1_n3.animate.set_color(GRAY), # Nodo isolato/spento
            c1_center.animate.set_color(BLUE) # DB Protetto/Ripristinato
        )
        self.play(Flash(c1_center, color=GREEN, flash_radius=0.5))
        
        final_text = Text("System Secured", font_size=30, color=GREEN).move_to([0, -3, 0])
        self.play(Write(final_text))
        
        self.wait(3)