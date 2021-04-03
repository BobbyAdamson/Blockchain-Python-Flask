import hashlib
import json
from time import time

class Blockchain(object):
  def __init__(self):
    self.chain = []
    self.current_transactions = []
    self.new_block(previous_hash=1, proof=100) # Genesis block

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

  @property
  def last_block(self):
    return self.chain[-1]

  @staticmethod
  def hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()