import arcade
from collections import deque

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FONT_SIZE = 30
LINES_PER_SCREEN = 5
FADE_DURATION = 2
LINE_HEIGHT = 80
AUTO_STABLE_DURATION = 3

class Viewer(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Viewer")
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        
        arcade.load_font("HeirofLightOTFRegular.otf")
        self.font = "Heir of Light OTF"
        
        self.text = self.read_text_file("news.txt")
        
        self.lines = deque()
        self.current_lines = []
        self.next_lines = []
        self.fade_time = 0
        self.total_time = 0
        self.stable_start_time = 0  # stable 상태 시작 시간 추가
        
        self.auto_mode = False
        self.auto_button_center = (SCREEN_WIDTH - 40, 0)
        self.auto_button_radius = 30
        
        self.state = "FADING_IN"  # "STABLE", "FADING_IN", "FADING_OUT"
        
        self.prepare_text()
        
    def read_text_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().replace("\n\n", "\n")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return "파일을 찾을 수 없습니다."
        except Exception as e:
            print(f"Error reading file: {e}")
            return "파일을 읽는 중 오류가 발생했습니다."
    
    def prepare_text(self):
        max_chars = (SCREEN_WIDTH - 100) // (FONT_SIZE * 1.1)
        for paragraph in self.text.split('\n'):
            words = paragraph.split()
            current_line = []
            current_length = 0
            for word in words:
                if current_length + len(word) + 1 <= max_chars:
                    current_line.append(word)
                    current_length += len(word) + 1
                else:
                    self.lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word)
            if current_line:
                self.lines.append(' '.join(current_line))
            self.lines.append('')
        self.advance_text()
        
    def on_draw(self):
        arcade.start_render()
        
        if self.state == "STABLE" or self.state == "FADING_OUT":
            opacity = 255 if self.state == "STABLE" else max(0, 255 * (1 - (self.total_time - self.fade_time) / FADE_DURATION))
            for i, line in enumerate(self.current_lines):
                arcade.draw_text(line, 100, SCREEN_HEIGHT - 130 - i * LINE_HEIGHT,
                                 arcade.color.WHITE + (int(opacity),), 
                                 font_size=FONT_SIZE, anchor_y="top", font_name=self.font)
        
        if self.state == "FADING_IN":
            opacity = min(255, 255 * (self.total_time - self.fade_time) / FADE_DURATION)
            for i, line in enumerate(self.current_lines):
                arcade.draw_text(line, 100, SCREEN_HEIGHT - 130 - i * LINE_HEIGHT,
                                 arcade.color.WHITE + (int(opacity),), 
                                 font_size=FONT_SIZE, anchor_y="top", font_name=self.font)
        
        # Auto 버튼 그리기
        if self.auto_mode:
            arcade.draw_text("Auto", self.auto_button_center[0], self.auto_button_center[1] + 30, 
                         arcade.color.WHITE, 20, anchor_x="center", anchor_y="center", font_name=self.font)
        else:
            arcade.draw_text("Auto", self.auto_button_center[0], self.auto_button_center[1] + 30, 
                         arcade.color.GRAY, 20, anchor_x="center", anchor_y="center", font_name=self.font)
    
    def on_update(self, delta_time):
        self.total_time += delta_time
        
        if self.state == "FADING_IN" and self.total_time - self.fade_time > FADE_DURATION:
            self.state = "STABLE"
            self.stable_start_time = self.total_time  # stable 상태 시작 시간 기록
        elif self.state == "FADING_OUT" and self.total_time - self.fade_time > FADE_DURATION:
            self.state = "FADING_IN"
            self.current_lines = self.next_lines
            self.next_lines = []
            self.fade_time = self.total_time
        
        if self.auto_mode and self.state == "STABLE":
            if self.total_time - self.stable_start_time >= AUTO_STABLE_DURATION:
                self.start_fade_out()
    
    def advance_text(self):
        if self.lines:
            self.next_lines = [self.lines.popleft() for _ in range(min(LINES_PER_SCREEN, len(self.lines)))]
            if not self.current_lines:
                self.state = "FADING_IN"
                self.current_lines = self.next_lines
                self.next_lines = []
                self.fade_time = self.total_time
            else:
                self.state = "FADING_OUT"
                self.fade_time = self.total_time
    
    def start_fade_out(self):
        if self.state == "STABLE":
            self.state = "FADING_OUT"
            self.fade_time = self.total_time
            self.advance_text()
    
    def on_mouse_press(self, x, y, button, modifiers):
        if ((x - self.auto_button_center[0])**2 + (y - self.auto_button_center[1])**2 <= self.auto_button_radius**2):
            self.auto_mode = not self.auto_mode
        elif not self.auto_mode and self.state == "STABLE":
            self.start_fade_out()

def main():
    window = Viewer()
    arcade.run()

if __name__ == "__main__":
    main()
