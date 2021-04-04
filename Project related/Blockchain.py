import hashlib
import json
import requests
from urllib.parse import urlparse
from time import time

class Blockchain(object):
  def __init__(self):
    self.chain = []
    self.current_transactions = []
    self.new_block(previous_hash=1, proof=100) # Genesis block

    self.nodes = set()

  def new_block(self, proof, previous_hash=None):
    block = {
      'index': len(self.chain) + 1,
      'timestamp': time(),
      'transactions': self.current_transactions,
      'proof': proof,
      'previous_hash': previous_hash or self.hash(self.chain[-1])
    }

    self.current_transactions = []
    self.chain.append(block)

    return block

  def new_transaction(self, sender, recipient, amount):
    self.current_transactions.append({
      'sender': sender,
      'recipient': recipient,
      'amount': amount
    })

    return self.last_block['index'] + 1

  def proof_of_work(self, last_proof):
    """
    Simple Proof of Work Algorithm:
      - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
      - p is the previous proof, and p' is the new proof
    :param last_proof: <int>
    :return: <int>
    """
    
    potential_new_proof = 0

    while self.valid_proof(last_proof, potential_new_proof) is False:
      potential_new_proof += 1

    new_proof = potential_new_proof
    return new_proof

  @staticmethod
  def valid_proof(last_proof, new_proof):
    """
    Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
    :param last_proof: <int> Previous Proof
    :param new_proof: <int> Current Proof
    :return: <bool> True if correct, False if not.
    """
    
    guess = f'{last_proof}{new_proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"

  def register_node(self, address):
    """
    Add a new node with an address
    """
    parsed_url = urlparse(address)
    self.nodes.add(parsed_url.netloc)

  def valid_chain(self, chain):
    """
    Checks if the chain passed is valid.
    :return: <bool> True if chain is valid, false if not
    """

    previous_block = chain[0]
    current_index = 1

    while current_index < len(chain):
      block_under_test = chain[current_index]
      print(f'Last block: {previous_block}')
      print(f'Current block on chain under test: {block_under_test}')
      print("\n--------------\n")
      
      # Check that the block hash is correct
      if block_under_test['previous_hash'] != self.hash(previous_block):
        return False

      # Check that the Proof of Work is correct
      if not self.valid_proof(previous_block['proof'], block_under_test['proof']):
        return False

      previous_block = block_under_test
      current_index +=1

    return True
  
  def resolve_conflicts(self):
    """
    The consensus algorithm. Resolves conflicts keeping the longest chain in state
    :return: <bool> True if chain was replaced, False if not
    """
    
    nodes_on_network = self.nodes
    new_chain = None

    # Keep track of the longest chain we find
    max_length = len(self.chain)

    # Fetch all chains from all nodes
    for node in nodes_on_network:
      response = requests.get(f'http://{node}/chain')

      if response.status_code == 200:
        response_json = response.json()
        neighbor_node_length = response_json['length']
        neighbor_node_chain = response_json['chain']

        if neighbor_node_length > max_length and self.valid_chain(neighbor_node_chain):
          max_length = neighbor_node_length
          new_chain = neighbor_node_chain

    if new_chain:
      self.chain = new_chain
      return True

    return False

  @property
  def last_block(self):
    return self.chain[-1]

  @staticmethod
  def hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()