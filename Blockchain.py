from hash_util import hash_string_256, hash_block
from collections import OrderedDict
from random import randrange
from random import uniform
from random import sample
from random import seed
import functools
import hashlib
import pickle
import random
import json
import csv

MINING_REWARD = 10
seed(1)

genesis_block = {
    'previous_hash': '', 
    'index': 0, 
    'transactions': [],
    'proof': 100
}

blockchain = [genesis_block]
open_transactions = []
owner = '0x1a2b33ff6f016342d1275be946166cff975c8b27542de70a7113ac6d1ef3294f'

content = ['fa1453bcbc919cfb64f62de736d55cf79e3d535b474ace256b4fbb56073f64db', '00000000f824d643f525b4904ea25c92174b8499435f388549a1700f4d3244de', 
        'fff122349700ff3494f215c412cd8c0ceabf1deb0df03ce39bcfc223b769d3c4', '00000000ddd96d128e122d1179034ff66c27dc583eb9e8996a0b1779c60c6f86',
        'abcd123fe5cb7c6c273547b0c9421b01e23310ed83f934b96270f35a4d66f6e3', '000000007c19ee8e924d3024d58efff50f872aadf256140bb1e3d62fea4fd6dd',
        '1345afdea87073ea3d7af299e02a434598b9c92094afa552e0711afcc0857962', '00000000ad2b48c7032b6d7d4f2e19e54d79b1c159f5599056492f2cd7bb528b',
        '9876123fa73fb23b6c42b18b3253ed29c5d0c80d84624efa12c2cf05c4b4318f', '00000000314e90489514c787d615cea50003af2023796ccdd085b6bcc1fa28f5',
        'ffaabed2b572a465b4e816420d47a16274557b3573b7924b64808a82c7322d9b', '00000000ac21f2862aaab177fd3c5c8b395de842f84d88c9cf3420b2d393e550',
        'ffff12222978eecde8d020f7f057083bc990002fff495121d7dc1c26d00c00f8', '000000009189006e461d2f4037a819d00217412ac01900ddbf09461100b836bb',
        'aaff23fe63d334becd1f17db9b6ccf570805caeed92d37d3d67b48e3685e760d']


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:4] == '0000' 
    

def validProof(transactions):
    guess = (str(transactions)).encode()
    guess_hash = hash_string_256(guess)
    return guess_hash


def validTarget(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    return guess_hash


def proof_of_work():
    open_transactions = [random.sample(content,10)]
    last_block = blockchain[-1]
    ind = last_block['index']
    last_hash = hash_block(last_block)
    proof = 0
    dummy = []
    with open('simBlockchainData.csv', mode='a', newline='') as sim:
        sim = csv.writer(sim, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        while not valid_proof(open_transactions, last_hash, proof):
            proof += 1
        sim.writerow([validProof(open_transactions),last_hash,proof,validTarget(open_transactions, last_hash, proof)])
        # for using timestamps :: import time and use, ts = time.time()
        return proof


def mine_block():
    for i in range(0,1000):
        last_block = blockchain[-1]
        hashed_block = hash_block(last_block)
        proof = proof_of_work()
        reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', 'where'), ('amount', MINING_REWARD)])
        copied_transactions = open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = {
            'previous_hash': hashed_block, 
            'index': len(blockchain), 
            'transactions': copied_transactions,   
            'proof': proof
        } 
        blockchain.append(block)
    return True
    

def get_user_choice():
    user_input = input('Your choice: ')
    return user_input

waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Mine a new block')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        if mine_block():
            open_transactions = []  
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Invalid input, please pick a value from the list!')
else:
    print('User left!')

print('Done!')  