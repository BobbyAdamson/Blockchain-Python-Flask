## Learning how to build a basic blockchain with Python

Following this guide: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

## To run:

In project directory run `python Project\ related/FlaskApp.py`

You can change the port you run on in the `run` method at the end of `FlaskApp.py`

## Endpoints

[GET] `/mine` - Prompts the program to run the proof of work algorithm, and when it finds the correct proof, claim the reward and add a new block to the chain

[GET] `/chain` - Gets the full chain

[POST] `/nodes/register` - Send an array of node addresses to register with the other nodes

[GET] `/nodes/resolve` - Triggers consensus algorithm to ensure the longest chain among all registered nodes has authority

## To do:

- Transaction validation
- Automatic consensus trigger on mining
- Use python conventions (I am not very familiar with python as of this project)

### Structure

- `Project related` - Directly related to the blockchain being built
- `Learning tools` - Examples and other sandboxes to demonstrate/learn specific concepts in isolation
