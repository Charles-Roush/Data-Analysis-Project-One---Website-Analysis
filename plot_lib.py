import matplotx # pyright: ignore[reportMissingImports]
import matplotlib.pyplot as plt
import matplotlib as mpl
import math

style = matplotx.styles.duftify(matplotx.styles.dracula)
mpl.style.use(style)


class Plot:
    def __init__(self, x_vals, y_vals = None, title="", x_title="", y_title=""):
        self.x_vals = x_vals
        self.y_vals = y_vals
        self.title = title
        self.x_title = x_title
        self.y_title = y_title

    def plot(self, ax):
        if self.title:
            ax.set_title(self.title)
        if self.x_title:
            ax.set_xlabel(self.x_title)
        if self.y_title:
            ax.set_ylabel(self.y_title)
        
        self._plot(ax)

    def _plot(self, ax):
        raise NotImplementedError("Subclasses gotta implement this")

class LinePlot(Plot):
    def _plot(self, ax):
        if self.y_vals:
            ax.plot(self.x_vals, self.y_vals)
        else:
            ax.plot(self.x_vals)

class HistPlot(Plot):
    def __init__(self, x_vals, bins=10, **kwargs):
        super().__init__(x_vals, **kwargs)
        self.bins = bins

    def _plot(self, ax):
        ax.hist(self.x_vals, bins=self.bins)


class PiePlot(Plot):
    def __init__(self, x_vals, labels=None, **kwargs):
        super().__init__(x_vals, **kwargs)
        self.labels = labels

    def _plot(self, ax):
        ax.pie(self.x_vals, labels=self.labels)


class BoxPlot(Plot):
    def _plot(self, ax):
        ax.boxplot(self.x_vals)

class SubPlot:
    def __init__(self, plots, rows=None, columns=None, size = (10, 4)):
        self.plots = plots
        self.n = len(plots)
        if rows is None and columns is None:
            self.rows = int(math.sqrt(self.n))
            self.columns = math.ceil(self.n / self.rows)
        elif rows is not None and columns is None:
            self.rows = rows
            self.columns = math.ceil(self.n / rows)
        elif rows is None and columns is not None:
            self.columns = columns
            self.rows = math.ceil(self.n / columns)
        else:
            self.rows = rows
            self.columns = columns

        self.fig, self.axes = plt.subplots(self.rows, self.columns, squeeze=False)

    def plot(self):
        axes_flat = self.axes.flatten()
        for ax, plot in zip(axes_flat, self.plots):
            plot.plot(ax)
        # Hide unused axes
        for ax in axes_flat[len(self.plots):]:
            self.fig.delaxes(ax)

        plt.tight_layout()
        file_title = 'no_title'
        if self.plots[0].title:
            file_title = self.plots[0].title
        path = f'plots/{file_title}.png'
        self.fig.savefig(path, bbox_inches="tight")
        plt.show()
        plt.close(self.fig)