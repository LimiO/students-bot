class Limiter:
    def reduce(self, quantity: int):
        self.limit -= quantity
        if not self.limit:
            self.delete_instance()
            return
        self.save()