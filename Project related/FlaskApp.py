import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from Blockchain import Blockchain

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
our_node_id = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
  # Get next proof
  last_block = blockchain.last_block
  last_proof = last_block['proof']
  new_proof = blockchain.proof_of_work(last_proof)

  # Received reward for finding the proof
  # Sender = 0 to signify this node has MINED a new coin (rather than receiving it in a transaction from another coin holder)
  blockchain.new_transaction(
    sender="0",
    recipient=our_node_id,
    amount=1
  )

  # Now that we've found the proof and received our reward...
  # Add the new block to the chain
  previous_hash = blockchain.hash(last_block)
  new_block = blockchain.new_block(new_proof, previous_hash)

  response = {
    'message': "New block added",
    'index': new_block['index'],
    'transactions': new_block['transactions'],
    'proof': new_block['proof'],
    'previous_hash': new_block['previous_hash'],
  }
  return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
  values = request.get_json()

  required = ['sender', 'recipient', 'amount']
  if not all(field in values for field in required):
    return 'Missing required fields', 400

  sender, recipient, amount = values.values()

  index = blockchain.new_transaction(sender, recipient, amount)

  response = {'message': f'Transaction will be added to block {index}'}
  return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
  response = {
    'chain': blockchain.chain,
    'length': len(blockchain.chain)
  }

  return jsonify(response), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=1337)