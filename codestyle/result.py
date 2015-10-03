from abc import ABCMeta, abstractmethod, abstractproperty


class BaseResult:
    """
    Base checking result
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_success(self):
        return False

    @abstractproperty
    def output(self):
        return ""

    def __bool__(self):
        return self.is_success()


class Result(BaseResult):
    """
    Code checking result
    """

    target = ""
    status = -1
    output = ""
    _is_success = False

    def __init__(self, target=None, status=None, output=""):
        self.target = target
        self.status = int(status)
        self.output = str(output) if output is not None else ""
        self._is_success = True if self.status == 0 else False

    def is_success(self):
        return self._is_success


class ResultSet(BaseResult):
    """
    Set of code checking results
    """

    def __init__(self):
        self.results = []

    def add(self, result):
        self.results.append(result)

    @property
    def output(self):
        output = ""
        for result in self.results:
            output += result.output
            if not output.endswith('\n'):
                output += '\n'
        return output

    def is_success(self):
        if len(self.results) == 0:
            return False
        is_success = True
        for result in self.results:
            if not result.is_success():
                is_success = False
                break
        return is_success