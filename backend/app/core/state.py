from collections import deque
from app.core.config import WINDOW_SIZE

mq_buffer = deque(maxlen=WINDOW_SIZE)
