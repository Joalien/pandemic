from pandemic.view.OutputView.OutputView import OutputView


class ConsoleOutputView(OutputView):
    def show_message(self, message: str) -> None:
        print(message)
