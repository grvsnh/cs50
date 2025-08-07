from fpdf import FPDF

class Shirtificate:
    def __init__(self, name):
        self.name = name
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.generate()

    @classmethod
    def get(cls):
        name = input("Name: ").strip()
        return cls(name)

    def generate(self):
        self.pdf.add_page()
        self.pdf.set_auto_page_break(auto=False, margin=0)

        self.pdf.set_font("Helvetica", "B", 50)
        title = "CS50 Shirtificate"
        title_width = self.pdf.get_string_width(title)
        x_title = (self.pdf.w - title_width) / 2
        self.pdf.set_xy(x_title, 20)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(title_width, 20, txt=title)

        img_width = 200
        img_x = (self.pdf.w - img_width) / 2
        self.pdf.image("shirtificate.png", x=img_x, y=60, w=img_width)

        self.pdf.set_font("Helvetica", "B", 30)
        name_text = f"{self.name} took CS50"
        name_width = self.pdf.get_string_width(name_text)
        x_name = (self.pdf.w - name_width) / 2
        self.pdf.set_xy(x_name, 130)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.cell(name_width, 20, txt=name_text)

        self.pdf.output("shirtificate.pdf")

def main():
    Shirtificate.get()

if __name__ == "__main__":
    main()
