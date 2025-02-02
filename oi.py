import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime

# Initialize data lists
strike_23000_data = []
strike_24000_data = []
time_series = []

# Function to generate random open interest data
def generate_open_interest_data():
    return random.randint(1000, 5000)

# Function to update the data and plot
def update(frame):
    current_time = datetime.datetime.now()
    time_series.append(current_time)
    
    # Generate random data for both strike prices
    strike_23000_data.append(generate_open_interest_data())
    strike_24000_data.append(generate_open_interest_data())

    # Keep only the last 50 data points
    if len(time_series) > 50:
        time_series.pop(0)
        strike_23000_data.pop(0)
        strike_24000_data.pop(0)

    # Clear and update the plot
    ax.clear()
    ax.plot(time_series, strike_23000_data, label='Strike Price 23000', marker='o')
    ax.plot(time_series, strike_24000_data, label='Strike Price 24000', marker='x')
    
    ax.set_title('Real-Time Open Interest for Strike Prices 23000 and 24000')
    ax.set_xlabel('Time')
    ax.set_ylabel('Open Interest')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45, ha='right')

# Set up the plot
fig, ax = plt.subplots(figsize=(12, 6))
ani = animation.FuncAnimation(fig, update, interval=5000)

# Display the plot
plt.tight_layout()
plt.show()