import sys
import tty
import termios


def get_key():
    """Wait for a keypress and return a single character string."""
    fd = sys.stdin.fileno()
    original_attributes = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, original_attributes)
    return ch


if __name__ == "__main__":
    print(get_key())
