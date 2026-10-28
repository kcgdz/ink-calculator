import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

class AppTests(unittest.TestCase):
    def test_calculation_and_density_shortcut(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'ink_calculator.py')).run()
        self.assertFalse(app.exception)
        next(b for b in app.button if b.label == '0.70').click().run()
        density = next(n for n in app.number_input if n.label == 'Ink Density (g/m²)')
        self.assertAlmostEqual(density.value, 0.7)
        next(b for b in app.button if b.label == 'Calculate').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.session_state['consumption_history']), 1)

if __name__ == '__main__':
    unittest.main()

