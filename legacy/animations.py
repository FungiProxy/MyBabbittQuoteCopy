class UIAnimations:
    @staticmethod
    def get_transition_stylesheet():
        return """
        QPushButton {
            transition: all 0.2s ease-in-out;
        }
        QPushButton:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        QListWidget::item {
            transition: background-color 0.15s ease;
        }
        QStackedWidget {
            transition: opacity 0.3s ease-in-out;
        }
        """