import pygame

from lab2.algorithms.base import DiskAccessAlgorithm

WIN_WIDTH = 1800
WIN_HEIGHT = 1000
CHAMBER_SIZE = 10
FPS = 15
COLORS = {
    'background': (0, 0, 0),
    'chamber': (100, 100, 100),
    'head': (0, 255, 0),
    'request': (255, 255, 255),
    'completed': (0, 255, 0),
    'current': (255, 0, 255),
    'failed': (255, 0, 0),
    'text': (255, 255, 255)
}

CHAMBER_HEIGHT = WIN_HEIGHT * 3 // 4


def generate_queue_with_failed_requests(algorithm: DiskAccessAlgorithm):
    queue = algorithm.generate_queue()
    for request in algorithm.requests:
        if request.failed:
            queue.append(request)
    return queue


class SimulationVisualizer:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Systemy Operacyjne | Lab 2")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        self.fps = FPS
        self.button_font = pygame.font.SysFont('Arial', 24)
        self.button_inc = pygame.Rect(WIN_WIDTH - 120, 20, 40, 40)
        self.button_dec = pygame.Rect(WIN_WIDTH - 60, 20, 40, 40)

    def draw_chambers(self, algorithm: DiskAccessAlgorithm):
        spacing = WIN_WIDTH / algorithm.num_chambers

        # track
        pygame.draw.rect(self.win, COLORS['chamber'],
                         (0, CHAMBER_HEIGHT - 2, WIN_WIDTH, 4))

        # markers
        for i in range(algorithm.num_chambers):
            mark_pos = int(i * spacing)
            pygame.draw.line(self.win, COLORS['chamber'],
                             (mark_pos, CHAMBER_HEIGHT - 10),
                             (mark_pos, CHAMBER_HEIGHT + 10), 1)

    def draw_needle(self, algorithm: DiskAccessAlgorithm):
        spacing = WIN_WIDTH / algorithm.num_chambers
        head_pos = int(algorithm.current_chamber * spacing)
        needle_width = 10
        needle_height = 40
        pygame.draw.rect(self.win, COLORS['head'],
                         (
                             head_pos - needle_width // 2, CHAMBER_HEIGHT - needle_height // 2,
                             needle_width,
                             needle_height))

    def draw_fps_buttons(self):
        # +
        pygame.draw.rect(self.win, (50, 200, 50), self.button_inc)
        plus_text = self.button_font.render("+", True, (255, 255, 255))
        self.win.blit(plus_text, (self.button_inc.x + 12, self.button_inc.y + 5))

        # -
        pygame.draw.rect(self.win, (200, 50, 50), self.button_dec)
        minus_text = self.button_font.render("-", True, (255, 255, 255))
        self.win.blit(minus_text, (self.button_dec.x + 14, self.button_dec.y + 5))

        # current FPS
        fps_text = self.font.render(f"FPS: {self.fps}", True, COLORS['text'])
        self.win.blit(fps_text, (WIN_WIDTH - 200, 30))

    def draw_requests(self, algorithm: DiskAccessAlgorithm):
        for request in reversed(generate_queue_with_failed_requests(algorithm)):
            position = (request.chamber / algorithm.num_chambers) * WIN_WIDTH
            y_pos = WIN_HEIGHT * 3 // 4

            if request.failed:
                color = COLORS['failed']
            elif request.arrival_time > algorithm.current_time:
                color = COLORS['completed']
            elif request == algorithm.current_request:
                color = COLORS['current']
            else:
                color = COLORS['request']

            pygame.draw.circle(self.win, color,
                               (int(position), y_pos), 8)
            if request.deadline > -1:
                deadline_text = self.font.render(str(request.deadline), True, color)
                self.win.blit(deadline_text, (int(position) - deadline_text.get_width() // 2, y_pos + 30))

    def draw_stats(self, algorithm: DiskAccessAlgorithm):
        stats = [
            f"Algorithm: {algorithm.__class__.__name__}",
            f"Time: {algorithm.current_time}",
            f"Current Chamber: {algorithm.current_chamber}",
            f"Target Chamber: {"<None>" if algorithm.current_request is None else algorithm.current_request.chamber}",
            f"Pending Requests: {sum(1 for r in algorithm.requests if not r.time_completed and not r.failed)}",
            f"Queued Requests: {len(algorithm.queue)}",
            f"Completed: {sum(1 for r in algorithm.requests if r.time_completed)}",
            f"Failed: {sum(1 for r in algorithm.requests if r.failed)}"
        ]

        y_offset = 10
        for stat in stats:
            text = self.font.render(stat, True, COLORS['text'])
            self.win.blit(text, (10, y_offset))
            y_offset += 25

    def draw_state(self, algorithm: DiskAccessAlgorithm):
        self.win.fill(COLORS['background'])
        self.draw_chambers(algorithm)
        self.draw_requests(algorithm)
        self.draw_needle(algorithm)
        self.draw_stats(algorithm)
        self.draw_fps_buttons()

        pygame.display.flip()
        self.clock.tick(self.fps)
        # pygame.display.update()

    def run(self, algorithm: DiskAccessAlgorithm):
        running = True
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.button_inc.collidepoint(event.pos):
                            self.fps = min(self.fps + 10, 240)  # Cap at 240 FPS
                        elif self.button_dec.collidepoint(event.pos):
                            self.fps = max(self.fps - 10, 1)  # Minimum 1 FPS

                # Update simulation
                if algorithm.has_pending_requests():
                    algorithm.tick()
                    self.draw_state(algorithm)
                else:
                    running = False
        except KeyboardInterrupt:
            print("Received Ctrl+C")
