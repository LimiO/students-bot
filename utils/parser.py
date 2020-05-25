from misc import langs


class Parser:
    @staticmethod
    def get_translation_args(text):
        split = text.split()
        if len(split) == 1:
            return [split[0]]
        elif len(split) == 2:
            if split[-1] in langs:
                return [split[0], split[1]]
            else:
                return [text]
        else:
            if split[-1] in langs and split[-2] in langs:
                return [' '.join(split[:-2]), split[-2], split[-1]]
            elif split[-1] in langs and split[-2] not in langs:
                return [' '.join(split[:-1]), split[-1]]
            else:
                return [text]

    @staticmethod
    def get_solution(text):
        pass
