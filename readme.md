nvidia-top
==========

For research, I deal with a lot of CUDA development and over time I realized that it was inconvenient to use nvidia-smi to monitor GPU usage and status. I was looking for a tool similar to the top command but for GPUs but was unable to find one. So I decided to write nvidia-top to monitor GPU/GPUs in a continuous manner similar to the top command.

Note that this tool only monitors NVIDIA GPUs which nvidia-smi can detect. It is written in python and requires the curses package to manage the output.

I plan to add additional functionality as I find more time. If you feel like something would be particularly useful and would like me to consider adding then email me at ab9 [at] mit.edu.