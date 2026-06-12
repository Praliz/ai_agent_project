# ai_agent_by_praliz
A fun project, building an agent which can read and write in files and run python.

The agent is even able to fix bug´s inside its own programs.

the example i used was to make a mistake in the calculator, and then requesting the agent to fix it.
it then automatically goes into the relevant files, tests my request case to fix the bug.
i hard coded the iterations to be 20 to keep it simple. the test i described took the following request around 4 iterations to fix.
"uv run main.py "i have a bug in my calculator.py 3 + 7 * 2 gives 20 which is wrong, please find the bug and fix it" --verbose.
have fun :D dont forget to use an API Key for Gemini for this to work. and install "uv"
