import os

if os.environ.get("POSTGRES_URL", None) in (None, ""):

    print("\n *** CAUTION ***")
    print("""
        In order to connect to the nesp2 se4all database
        you need to provide values to the following environment variables:\n
        POSTGRES_URL, POSTGRES_USER, POSTGRES_PW, POSTGRES_DB.\n
        You can do so by copying the following lines (without empty lines):
        """
    )

    print("""
--build-arg POSTGRES_URL=<>
--build-arg POSTGRES_USER=<>
--build-arg POSTGRES_PW=<>
--build-arg POSTGRES_DB=<>
    """
    )
    print("""
       Into a file (for example docker_inputs.txt) and feed it to the docker command with
sudo docker build -t nesp2_website $(< docker_inputs.txt) .
        Note that the '.' at the end of the previous line is important!
        """
    )
    print("\n *** CAUTION ***")