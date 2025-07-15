def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(str(e).strip("'"))
        except IndexError:
            print("Missing required arguments. Please provide all the arguments.")
        except KeyError:
            print("Record with given name doesn't exist.")
        except Exception as e:
            print(f"Unknown error: {e}")

    return inner
