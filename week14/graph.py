import csv
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


CHART_TYPES = (
	"Scatter",
	"Bar",
	"Horizontal bar",
	"Line",
	"Multiple lines",
	"Marker",
	"Histogram",
	"Pie",
	"Exploded pie",
	"Pie with legend",
)

DEFAULT_CHARTS = [
	("Scatter", "Scatter Plot: Color Values", "X", "Y", "5, 7, 8, 7, 2, 17, 2, 9, 4, 11, 12, 9, 6", "99, 86, 87, 88, 111, 86, 103, 87, 94, 78, 77, 85, 86", "0, 10, 20, 30, 40, 45, 50, 55, 60, 70, 80, 90, 100", ""),
	("Scatter", "Scatter Plot: Color and Size", "X", "Y", "8, 15, 22, 29, 36, 43, 50, 57", "31, 76, 48, 91, 55, 68, 24, 83", "10, 25, 40, 55, 70, 85, 100, 115", "20, 40, 60, 80, 100, 120, 140, 160"),
	("Horizontal bar", "Horizontal Bar Chart", "Category", "Value", "A, B, C, D", "3, 8, 1, 10", "", ""),
	("Line", "Sports Watch Data", "Average Pulse", "Calorie Burnage", "80, 85, 90, 95, 100, 105, 110, 115, 120, 125", "240, 250, 260, 270, 280, 290, 300, 310, 320, 330", "", ""),
	("Multiple lines", "Two Line Series", "X", "Y", "0, 1, 2, 3", "3, 8, 1, 10", "6, 2, 7, 11", ""),
	("Marker", "Marker Plot", "Point", "Value", "", "3, 8, 1, 10", "", ""),
	("Histogram", "Histogram", "Value", "Frequency", "150, 156, 159, 162, 164, 166, 168, 169, 170, 171, 173, 175, 178, 181, 186", "", "", ""),
	("Exploded pie", "Exploded Pie Chart", "Category", "Value", "Apples, Bananas, Cherries, Dates", "35, 25, 25, 15", "", ""),
	("Pie with legend", "Pie Chart with Legend", "Category", "Value", "Apples, Bananas, Cherries, Dates", "35, 25, 25, 15", "", ""),
]


def split_values(text):
	values = next(csv.reader([text], skipinitialspace=True), [])
	values = [value.strip() for value in values if value.strip()]
	if not values:
		raise ValueError("Enter at least one value.")
	return values


def number_values(text):
	try:
		return [float(value) for value in split_values(text)]
	except ValueError as error:
		raise ValueError("Enter comma-separated numbers.") from error


def draw_chart(axis, chart_type, title, x_label, y_label, x_text, y_text, extra_text, size_text):
	axis.clear()
	axis.set_title(title)
	mappable = None

	if chart_type == "Scatter":
		x_values = number_values(x_text)
		y_values = number_values(y_text)
		if len(x_values) != len(y_values):
			raise ValueError("X and Y values must have the same length.")
		colors = number_values(extra_text) if extra_text.strip() else list(range(len(x_values)))
		if len(colors) != len(x_values):
			raise ValueError("Color values must match the number of points.")
		plot_options = {"c": colors, "cmap": "viridis"}
		if size_text.strip():
			sizes = number_values(size_text)
			if len(sizes) != len(x_values):
				raise ValueError("Point sizes must match the number of points.")
			if any(size < 0 for size in sizes):
				raise ValueError("Point sizes cannot be negative.")
			plot_options["s"] = sizes
		mappable = axis.scatter(x_values, y_values, **plot_options)
	elif chart_type in ("Bar", "Horizontal bar"):
		categories = split_values(x_text)
		values = number_values(y_text)
		if len(categories) != len(values):
			raise ValueError("Categories and values must have the same length.")
		if chart_type == "Bar":
			axis.bar(categories, values)
		else:
			axis.barh(categories, values)
	elif chart_type in ("Line", "Multiple lines"):
		x_values = number_values(x_text)
		y_values = number_values(y_text)
		if len(x_values) != len(y_values):
			raise ValueError("X and Y values must have the same length.")
		axis.plot(x_values, y_values, marker="o", label="Series 1")
		if chart_type == "Multiple lines":
			second_values = number_values(extra_text)
			if len(x_values) != len(second_values):
				raise ValueError("The second series must match the X values.")
			axis.plot(x_values, second_values, marker="s", label="Series 2")
			axis.legend()
		elif chart_type == "Line":
			axis.grid(True)
	elif chart_type == "Marker":
		values = number_values(y_text)
		axis.plot(range(len(values)), values, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
		axis.grid(True)
	elif chart_type == "Histogram":
		values = number_values(x_text)
		axis.hist(values, bins=min(15, len(values)), edgecolor="white")
	elif chart_type in ("Pie", "Exploded pie", "Pie with legend"):
		labels = split_values(x_text)
		values = number_values(y_text)
		if len(labels) != len(values):
			raise ValueError("Categories and values must have the same length.")
		if any(value < 0 for value in values) or sum(values) <= 0:
			raise ValueError("Pie values must be non-negative and add up to more than zero.")
		pie_options = {"labels": labels, "autopct": "%1.1f%%"}
		if chart_type == "Exploded pie":
			pie_options["explode"] = [0.2] + [0] * (len(values) - 1)
			pie_options["shadow"] = True
		wedges, _, _ = axis.pie(values, **pie_options)
		if chart_type == "Pie with legend":
			axis.legend(wedges, labels, loc="center left", bbox_to_anchor=(0.95, 0.5), fontsize=8)
	else:
		raise ValueError("Choose a chart type from the list.")

	if chart_type not in ("Pie", "Exploded pie", "Pie with legend"):
		axis.set_xlabel(x_label)
		axis.set_ylabel(y_label)
	return mappable


def main():
	root = tk.Tk()
	root.title("Customizable Graph Dashboard")
	root.geometry("1600x950")
	root.minsize(1200, 700)
	root.columnconfigure(1, weight=1)
	root.rowconfigure(0, weight=1)

	controls_canvas = tk.Canvas(root, width=410, highlightthickness=0)
	controls_scrollbar = ttk.Scrollbar(root, orient="vertical", command=controls_canvas.yview)
	controls_canvas.configure(yscrollcommand=controls_scrollbar.set)
	controls_canvas.grid(row=0, column=0, sticky="nsew")
	controls_scrollbar.grid(row=0, column=0, sticky="nse")
	controls = ttk.Frame(controls_canvas, padding=(10, 10, 24, 10))
	controls_window = controls_canvas.create_window((0, 0), window=controls, anchor="nw")

	def update_scroll_region(_event):
		controls_canvas.configure(scrollregion=controls_canvas.bbox("all"))

	def update_controls_width(event):
		controls_canvas.itemconfigure(controls_window, width=event.width)

	controls.bind("<Configure>", update_scroll_region)
	controls_canvas.bind("<Configure>", update_controls_width)
	ttk.Label(controls, text="Graph settings", font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 8))

	settings = []
	field_labels = (
		("title", "Title"),
		("x_label", "X-axis label"),
		("y_label", "Y-axis label"),
		("x_data", "X values / categories"),
		("y_data", "Y values"),
		("extra_data", "Colors / second series"),
		("size_data", "Point sizes"),
	)
	for index, defaults in enumerate(DEFAULT_CHARTS, start=1):
		chart_type, title, x_label, y_label, x_data, y_data, extra_data, size_data = defaults
		panel = ttk.LabelFrame(controls, text=f"Graph {index}", padding=8)
		panel.pack(fill="x", pady=5)
		setting = {
			"type": tk.StringVar(value=chart_type),
			"title": tk.StringVar(value=title),
			"x_label": tk.StringVar(value=x_label),
			"y_label": tk.StringVar(value=y_label),
			"x_data": tk.StringVar(value=x_data),
			"y_data": tk.StringVar(value=y_data),
			"extra_data": tk.StringVar(value=extra_data),
			"size_data": tk.StringVar(value=size_data),
		}
		settings.append(setting)

		ttk.Label(panel, text="Chart type").grid(row=0, column=0, sticky="w", pady=2)
		ttk.Combobox(panel, textvariable=setting["type"], values=CHART_TYPES, state="readonly").grid(
			row=0, column=1, sticky="ew", pady=2
		)
		for row, (key, label) in enumerate(field_labels, start=1):
			ttk.Label(panel, text=label).grid(row=row, column=0, sticky="w", pady=2)
			ttk.Entry(panel, textvariable=setting[key]).grid(row=row, column=1, sticky="ew", pady=2)
		panel.columnconfigure(1, weight=1)

	status = tk.StringVar(value="Enter comma-separated data, then select Update graphs.")
	status_label = ttk.Label(controls, textvariable=status, wraplength=360)
	status_label.pack(anchor="w", pady=(8, 4))

	chart_frame = ttk.Frame(root, padding=8)
	chart_frame.grid(row=0, column=1, sticky="nsew")
	chart_frame.rowconfigure(1, weight=1)
	chart_frame.columnconfigure(0, weight=1)
	figure = Figure(figsize=(11, 7), constrained_layout=True)
	figure.suptitle("My First Chart", fontsize=16)
	axes = figure.subplots(3, 3).flatten()
	chart_canvas = FigureCanvasTkAgg(figure, master=chart_frame)
	toolbar = NavigationToolbar2Tk(chart_canvas, chart_frame, pack_toolbar=False)
	toolbar.update()
	toolbar.grid(row=0, column=0, sticky="ew")
	chart_canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
	colorbars = [None] * len(axes)

	def update_graphs():
		errors = []
		for index, (axis, setting) in enumerate(zip(axes, settings)):
			if colorbars[index] is not None:
				colorbars[index].remove()
				colorbars[index] = None
			try:
				mappable = draw_chart(
					axis,
					setting["type"].get(),
					setting["title"].get(),
					setting["x_label"].get(),
					setting["y_label"].get(),
					setting["x_data"].get(),
					setting["y_data"].get(),
					setting["extra_data"].get(),
					setting["size_data"].get(),
				)
				if mappable is not None:
					colorbars[index] = figure.colorbar(mappable, ax=axis, shrink=0.8, label="Color value")
			except ValueError as error:
				axis.clear()
				axis.set_title(setting["title"].get())
				axis.text(0.5, 0.5, str(error), ha="center", va="center", wrap=True, color="crimson")
				axis.set_xticks([])
				axis.set_yticks([])
				errors.append(f"Graph {index + 1}: {error}")
		status.set(" | ".join(errors) if errors else "All graphs updated.")
		chart_canvas.draw_idle()

	ttk.Button(controls, text="Update graphs", command=update_graphs).pack(fill="x", pady=(4, 8))
	update_graphs()
	root.mainloop()


if __name__ == "__main__":
	main()