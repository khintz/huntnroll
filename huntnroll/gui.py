import random
import tkinter as tk
from tkinter import messagebox


def pick_uniform(names):
    n = len(names)
    if n != 2:
        raise ValueError("Exactly two names must be provided.")
    idx = random.randint(0, 1)
    return names[idx], idx


def draw_distribution(names, winner_idx):
    canvas.delete("all")
    n = len(names)
    width = 400
    height = 220
    margin = 40
    # Draw axis
    canvas.create_line(
        margin, height - margin, width - margin, height - margin, fill="#888"
    )
    # Draw uniform (flat) distribution
    for i in range(n):
        px = margin + (width - 2 * margin) * i / (n - 1 if n > 1 else 1)
        bar_top = height - margin - 100
        bar_bottom = height - margin
        color = "#1f77b4" if i != winner_idx else "red"
        canvas.create_rectangle(
            px - 8, bar_top, px + 8, bar_bottom, fill=color, outline="black"
        )
    # Draw name markers
    for i, name in enumerate(names):
        px = margin + (width - 2 * margin) * i / (n - 1 if n > 1 else 1)
        color = "red" if i == winner_idx else "black"
        canvas.create_text(
            px,
            height - margin + 15,
            text=str(i + 1),
            fill=color,
            font=("Arial", 8, "bold" if i == winner_idx else "normal"),
        )
        if n <= 10:
            canvas.create_text(
                px,
                height - margin + 35,
                text=name,
                fill=color,
                font=("Arial", 8),
            )


def select_winner():
    names = entry.get().split(",")
    names = [name.strip() for name in names if name.strip()]
    if len(names) != 2:
        messagebox.showerror(
            "Error", "Please enter exactly two names, separated by a comma."
        )
        return
    slot1 = slot1_var.get()
    slot2 = slot2_var.get()
    winner, idx = pick_uniform(names)
    loser = names[1 - idx]
    winner_slot = slot1 if idx == 0 else slot2
    loser_slot = "evening" if winner_slot == "morning" else "morning"
    stats = (
        f"Selected to start: {winner}\n"
        f"{names[0]} prefers: {slot1}\n"
        f"{names[1]} prefers: {slot2}\n"
        f"Day 1: {winner} ({winner_slot})\n"
        f"Day 1: {loser} ({loser_slot})\n"
        f"Then alternate full days."
    )
    result_var.set(stats)
    draw_distribution(names, idx)
    # Generate and display schedule for 14 days
    schedule = [
        f"Day 1: {winner} ({winner_slot})",
        f"Day 1: {loser} ({loser_slot})",
    ]
    for i in range(2, 15):
        person = winner if (i % 2 == 0) else loser
        schedule.append(f"Day {i}: {person}")
    schedule_var.set("\n".join(schedule))


root = tk.Tk()
root.title("Huntnroll - Who Starts?")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Enter exactly two names (comma separated):")
label.pack()

entry = tk.Entry(frame, width=60)
entry.pack(pady=5)


# Slot preferences for each name
slot_frame = tk.Frame(frame)
slot_frame.pack(pady=5)

slot1_var = tk.StringVar(value="morning")
slot2_var = tk.StringVar(value="evening")

slot1_label = tk.Label(slot_frame, text="First name prefers:")
slot1_label.grid(row=0, column=0, sticky="e")
slot1_morning = tk.Radiobutton(
    slot_frame, text="morning", variable=slot1_var, value="morning"
)
slot1_evening = tk.Radiobutton(
    slot_frame, text="evening", variable=slot1_var, value="evening"
)
slot1_morning.grid(row=0, column=1)
slot1_evening.grid(row=0, column=2)

slot2_label = tk.Label(slot_frame, text="Second name prefers:")
slot2_label.grid(row=1, column=0, sticky="e")
slot2_morning = tk.Radiobutton(
    slot_frame, text="morning", variable=slot2_var, value="morning"
)
slot2_evening = tk.Radiobutton(
    slot_frame, text="evening", variable=slot2_var, value="evening"
)
slot2_morning.grid(row=1, column=1)
slot2_evening.grid(row=1, column=2)

button = tk.Button(frame, text="Pick Winner", command=select_winner)
button.pack(pady=10)

result_var = tk.StringVar()
result_label = tk.Label(
    frame, textvariable=result_var, font=("Arial", 14, "bold"), fg="green"
)
result_label.pack(pady=10)

# Canvas for distribution plot
canvas = tk.Canvas(frame, width=400, height=220, bg="white")
canvas.pack(pady=10)

# Schedule output
schedule_var = tk.StringVar()
schedule_label = tk.Label(frame, textvariable=schedule_var, font=("Arial", 12))
schedule_label.pack(pady=10)

root.mainloop()
