class Files:
    @staticmethod
    def read_file(file_path: str) -> str:
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
