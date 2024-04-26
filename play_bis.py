##ELIE
from math import sqrt, log, copysign
import random ## pour les mouvements aleatoires
from deuces import Card, Deck, Evaluator ##pour les cartes
from random import shuffle
import copy
import numpy as np
import time
from graphviz import Digraph
import matplotlib.pyplot as plt
import networkx as nx





def signe(x):
    if x== 0:
        return 0
    return copysign(1,x)

class Deck:
    """
    Class representing a deck. The first time we create, we seed the static 
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it. 
    """
    _FULL_DECK = []

    def __init__(self):
        
        self.shuffle()

    def shuffle(self):
        # and then shuffle
        self.cards = Deck.GetFullDeck()
        shuffle(self.cards)

    def draw(self, n=1):
        if n == 1:
            return self.cards.pop(0)

        cards = []
        for i in range(n):
            cards.append(self.draw())
        return cards

    def __str__(self):
        return Card.print_pretty_cards(self.cards)
    
    def copy(self):
        return self.cards.copy()

    
    @staticmethod
    def GetFullDeck():
        if Deck._FULL_DECK:
            return list(Deck._FULL_DECK)

        # create the standard 52 card deck
        for rank in Card.STR_RANKS:
            for suit,val in Card.CHAR_SUIT_TO_INT_SUIT.items():
                Deck._FULL_DECK.append(Card.new(rank + suit))

        return list(Deck._FULL_DECK)



class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self):##, move = None, parent = None, state :'PokerState' = None): # mettre current state?
        self.parentNode = None # "None" for the root node
        self.childNodes = [] ## les nodes enfants
        self.wins = 0
        self.visits = 0
        self.current='preflop'
        self.hand=[]
        self.flop_cards=[]
        self.turn_card=[]
        self.river_card=[]
        self.opp_hand=[]
        self.community_cards=[]
        self.preflop_moves=''
        self.flop_moves=''
        self.turn_moves=''
        self.river_moves=''
        self.opp_preflop_moves=''
        self.opp_flop_moves=''
        self.opp_turn_moves=''
        self.opp_river_moves=''
        self.deck = Deck.GetFullDeck()#Elie
        random.shuffle(self.deck)
        self.reward = 0
        self.untried_moves = ["fold","check","raise"]
        #if pr remplir les cartes



    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        #if (random.random()<0.1):
            #s = random.choice(self.childNodes)
        #else:
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + 3*sqrt(2*log(self.visits)/c.visits))[-1]
        return s

    def clone(self):#effet de bord?
        # Création d'une nouvelle instance de la classe Node
        cloned_node = Node()  # state est None car playerJustMoved est déjà copié
        # Copie des valeurs des attributs
        #parent?
        cloned_node.childNodes = self.childNodes[:]  # Copie superficielle de la liste
        cloned_node.wins = self.wins
        cloned_node.visits = self.visits
        cloned_node.current = self.current
        cloned_node.hand = self.hand[:]
        cloned_node.flop_cards = self.flop_cards[:]
        cloned_node.turn_card = self.turn_card
        cloned_node.river_card = self.river_card
        cloned_node.opp_hand = self.opp_hand[:]
        cloned_node.community_cards = self.community_cards[:]
        cloned_node.preflop_moves = self.preflop_moves[:]
        cloned_node.flop_moves = self.flop_moves
        cloned_node.turn_moves = self.turn_moves
        cloned_node.river_moves = self.river_moves
        cloned_node.opp_preflop_moves = self.opp_preflop_moves
        cloned_node.opp_flop_moves = self.opp_flop_moves
        cloned_node.opp_turn_moves = self.opp_turn_moves
        cloned_node.opp_river_moves = self.opp_river_moves
        cloned_node.deck = self.deck
        cloned_node.untried_moves = self.untried_moves
        cloned_node.reward = self.reward
        return cloned_node
    
    def make_graph(self, graph=None):
        if graph is None:
            graph = Digraph(comment='Poker Game Tree')
            graph.attr('node', shape='ellipse')

        # Ajouter le noeud courant au graphique
        graph.node(name=str(id(self)),
                  label=f"W/V: {self.wins}/{self.visits}\nMoves: {self.preflop_moves}, {self.flop_moves}, {self.turn_moves}, {self.river_moves}")

        # Ajouter des arêtes et des noeuds enfants récursivement
        for child in self.childNodes:
            graph.edge(str(id(self)), str(id(child)))
            child.make_graph(graph)

        return graph

    def AddChild(self, s):##ici il me faut une maniere differentes d'ajouter un enfant
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
            Elie speaking:
            ##Idee: creer tte les nodes avec comme enfant (check, raise, fold) des le debut
            # on les mets dans Untried Move et apres on tire au hasard dans untried move en priorité?
        """
        ##la fonction initial def AddChild(self, m, s):##ici il me faut une maniere differentes d'ajouter un enfant
        ##il faudrait verifier qu'il n'a pas encore d'enfant avec les memes cartes
        for i in self.childNodes: ##on verfie qu'il n'existe pas deja des enfants contenant ces cartes et on traitera cela
            if(i.preflop_moves == s.preflop_moves and i.flop_moves == s.flop_moves and i.turn_moves == s.turn_moves and i.river_moves == s.river_moves):
                return
        self.childNodes.append(s)
        return n
    def IsAChild(self, s):##cette fonction permet de verifier si un noeud est deja un enfant # Elie: pq pas verifier avec self.parent
        for i in self.childNodes: ##on verfie qu'il n'existe pas deja des enfants contenant ces cartes et on traitera cela
            if(i.hand==s.hand): ## dans l'idee il faudrait comparer tous les etats du jeu
                return True
        return False

    ##def Update(self, result): #Elie: ou est le pb?
      ##  __init__(self, move = None, parent = None, state :'PokerState' = None)
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        ##self.visits += 1
        ##self.wins += result
    
    def find_move(self):
        if (self.river_moves !=''):
            return self.river_moves
        if (self.turn_moves !=''):
            return self.turn_moves
        if (self.flop_moves !=''):
            return self.flop_moves
        if (self.preflop_moves !=''):
            return self.preflop_moves

    def __repr__(self):
        return "[ W/V:" + str(self.wins) + "/" + str(self.visits)  + "]"
    
    def result(self):
        return np.array([self.wins,self.visits])

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s

    def backpropagate(self, reward):#Elie: on mets -1 pr la perte? et 0 pr egalité?
        """
        Update the win and visit count for the node. Propagate the update up to the root node.

        Args:
            is_win (bool): True if the current path resulted in a win, otherwise False.
        """
        self.wins += reward
        self.visits += 1

        if self.parentNode != None:
            self.parentNode.backpropagate(reward)

    def play(self): ## ici le but est d'entrainer notre arbre plusieurs fois pour qu'il puisse apprendre a jouer l'idee c'est qu'a chque modification on cree un enfant donc il faut etre meticuleux
        #print(self.current)
        #print(Card.print_pretty_cards(self.hand))
        #print(self.current)
        #if (self.opp_hand):
            #Card.print_pretty_cards(self.opp_hand) 

        #Card.print_pretty_cards(self.community_cards)
        
        if self.current=='preflop' :#avant de recevoir les cartes
            if self.hand==[]: ## la main est vide donc on ajoute les cartes du joueurs nous sommes donc dans la root
                self.hand.append(self.deck.pop())
                self.hand.append(self.deck.pop())
                self.opp_hand.append(Card.new('Ah'))
                self.opp_hand.append(Card.new('Ts'))
            
            
                
                # pas d'enfant on en cree un, mettre if untried moves pas vide apres
                # on a recu les cartes, et on tire ici les 3 du flop
               
            
            deck = copy.deepcopy(self.deck)
            random.shuffle(deck)
            #deck.shuffle()
            card_opp1 = deck.pop()
            card_opp2 = deck.pop()
            #self.opp_hand[0]=deck.pop() #ca compte pas
            #self.opp_hand[1] = deck.pop()

            card1 = deck.pop()
            card2 = deck.pop()
            #print(Card.print_pretty_card(card1))
            card3 = deck.pop()
            flop_cards = [card1, card2, card3]
            community_cards = [card1, card2, card3]
            

            if (self.untried_moves):
                my_choice = self.untried_moves.pop(random.randrange(0,len(self.untried_moves)))#take a random choice and pop it from untried_moves
            
                if (my_choice == 'dead end'):
                    self.untried_moves.append(my_choice) # On remets dead end psk c'est une feuille 
                    self.backpropagate(-1)

                elif (my_choice == 'fold'):
                    s=self.clone()
                    s.parentNode= self
                    s.flop_cards= flop_cards
                    s.community_cards = community_cards
                    s.opp_hand[0]= card_opp1
                    s.opp_hand[1] = card_opp2

                    s.childNodes = [] ## les nodes enfants
                    s.wins = 0
                    s.visits = 1
                    s.current='flop'
                    s.preflop_moves='fold'

                    s.deck = deck#Elie
                    s.untried_moves = ['dead end']#ends here
                    s.backpropagate(-1)
                    self.AddChild(s)
                    #self.play()

                else:#hypothese simplificatrice, soit nous suit soit fold, ie call peut etre bet en cas de raise
                    opp_choice= random.choice(['call','fold'])
                    self.opp_preflop_moves=opp_choice#le premier move ici
                    
                    s=self.clone()
                    s.parentNode= self
                    s.childNodes=[]
                    s.wins=0
                    s.visits=1
                    s.current='flop'
                    s.flop_cards= flop_cards
                    s.opp_hand[0]= card_opp1
                    s.opp_hand[1] = card_opp2
                    
                    s.community_cards = community_cards
                    s.deck = deck#Elie
                    
                    s.untried_moves = ["fold","check","raise"]
                    s.preflop_moves= my_choice
                    s.opp_preflop_moves= opp_choice

                    self.AddChild(s)
                    if(opp_choice=='fold'):
                        self.backpropagate(1)
                    else:
                        s.play()
            else:
                #if child Nodes n'est pas vide
                #s = random.choice(self.childNodes)
                s = self.UCTSelectChild()
                #s.visits = 0
                s.flop_cards=flop_cards
                s.community_cards=community_cards
                s.opp_hand[0]= card_opp1
                s.opp_hand[1] = card_opp2
                #determiner s.opp_moves
                #if fold backpropagate 1
                #else s.play()
                    
                s.deck = deck
                
                s.play()

        elif self.current=='flop':#il y a deja le flop, il faut tirer la turn pr la suite
            deck = copy.deepcopy(self.deck)
            random.shuffle(deck)

            turn_card= deck.pop()

            if (self.untried_moves):
                my_choice = self.untried_moves.pop(random.randrange(0,len(self.untried_moves)))#take a random choice and pop it from untried_moves
            
            
                if (my_choice == 'dead end'):
                    self.untried_moves.append(my_choice) # On remets dead end psk c'est une feuille 
                    self.backpropagate(-1)

                elif (my_choice=='fold'):
                    s=self.clone()
                    s.parentNode = self # "None" for the root node
                    s.childNodes = [] ## les nodes enfants
                    s.wins = 0
                    s.visits = 1
                    s.current='turn'
                    s.turn_card.append(turn_card)
                    
                    s.community_cards.append(turn_card)
                    
                    s.flop_moves=my_choice
                    
                    s.deck = deck#Elie
                    s.untried_moves = ['dead end']#ends here
                    s.backpropagate(-1)
                    self.AddChild(s)
                else:#hyp simplificatrice encore
                    opp_choice= random.choice(['call','fold'])
                    self.opp_flop_moves =opp_choice
                    
                    s=self.clone()
                    s.parentNode= self
                    s.childNodes=[]
                    s.wins=0
                    s.visits=1
                    s.current='turn'
                    s.turn_card=turn_card
                    s.community_cards.append(turn_card)
                    s.flop_moves=my_choice
                    s.opp_flop_moves=opp_choice
                    s.deck = deck
                    s.untried_moves = ["fold","check","raise"]
                    self.AddChild(s)
                    if(opp_choice=='fold'):
                        self.backpropagate(1)
                    else:
                        s.play()
            else:
                #if child Nodes n'est pas vide
                s = random.choice(self.childNodes)
                s = self.UCTSelectChild()
                
                s.community_cards = self.community_cards
                s.opp_hand = self.opp_hand
                s.turn_card = turn_card
                if(len(s.community_cards)!=3):
                    print("AKHAA")

                s.community_cards.append(turn_card)
                s.deck = deck
                s.play()


            
            
            
            
            
        elif self.current=='turn':
            deck = copy.deepcopy(self.deck)
            random.shuffle(deck)
            river_card= deck.pop()

            if (self.untried_moves):
                my_choice = self.untried_moves.pop(random.randrange(0,len(self.untried_moves)))#take a random choice and pop it from untried_moves
            
                if (my_choice == 'dead end'):
                    self.untried_moves.append(my_choice) # On remets dead end psk c'est une feuille 
                    self.backpropagate(-1)

                elif (my_choice=='fold'):
                    s=self.clone()
                    s.parentNode = self # "None" for the root node
                    s.childNodes = [] ## les nodes enfants
                    s.wins = 0
                    s.visits = 1
                    s.current='river'
                    s.river_card.append(river_card)
                    
                    s.community_cards.append(river_card)
                    
                    s.turn_moves=my_choice
                    
                    s.deck = deck#Elie
                    s.untried_moves = ['dead end']#ends here
                    s.backpropagate(-1)
                    self.AddChild(s)
                else:#hyp simplificatrice encore
                    opp_choice= random.choice(['call','fold'])
                    self.opp_turn_moves=opp_choice
                    
                    #on cree l'enfant et on continue
                    s=self.clone()
                    s.parentNode= self
                    s.childNodes=[]
                    s.wins=0
                    s.visits=1
                    s.current='river'
                    s.river_card = river_card
                    s.community_cards.append(river_card)
                    s.turn_moves=my_choice
                    s.opp_turn_moves=opp_choice
                    s.deck = deck
                    s.untried_moves = ["fold","check","raise"]
                    self.AddChild(s)
                    if(opp_choice=='fold'):
                        self.backpropagate(1)
                    else:
                        s.play()
            else:
                #if child Nodes n'est pas vide
                s = random.choice(self.childNodes)
                s = self.UCTSelectChild()
                s.community_cards = self.community_cards
                s.opp_hand = self.opp_hand
                if(len(s.community_cards)!=4):
                    print("AKHAAAAAAAA")
                s.river_card = river_card
                s.community_cards.append(river_card)
                s.deck = deck
                s.play()





            
                   



        elif self.current=='river':#la river est tirée, il faut faire un move
            if (self.untried_moves):
                my_choice = self.untried_moves.pop(random.randrange(0,len(self.untried_moves)))#take a random choice and pop it from untried_moves


                if (my_choice == 'dead end'):
                    self.untried_moves.append(my_choice) # On remets dead end psk c'est une feuille 
                    self.backpropagate(-1)
            
                elif (my_choice=='fold'):
                    s=self.clone()
                    s.parentNode = self # "None" for the root node
                    s.childNodes = [] ## les nodes enfants
                    s.wins = 0
                    s.visits = 1
                    s.current='showdown'
                    
                    s.river_moves=my_choice
                    
                    s.untried_moves = ['dead end']#ends here
                    s.backpropagate(-1)
                    self.AddChild(s)
                else:#hyp simplificatrice encore
                    opp_choice= random.choice(['call','fold'])
                    self.opp_river_moves =opp_choice
                
                    #on cree l'enfant et on continue
                    s=self.clone()
                    s.parentNode= self
                    s.childNodes=[]
                    s.wins=0
                    s.visits=1
                    s.current='showdown'
                    
                    s.river_moves=my_choice
                    s.opp_river_moves=opp_choice
                    
                    s.untried_moves = []#nothing else for now 
                    self.AddChild(s)
                    if(opp_choice=='fold'):
                        self.backpropagate(1)
                    else:
                        
                        s.play()
            else:
                #if child Nodes n'est pas vide
                s = random.choice(self.childNodes)
                s = self.UCTSelectChild()
                s.community_cards = self.community_cards
                s.opp_hand = self.opp_hand
                
                
                s.play()
                

            
            
            
            
        elif self.current=='showdown':
            
            

            evaluator = Evaluator()
            #tirer des cartes pr le opps
            #self.opp_hand.append(self.deck.pop())
            #self.opp_hand.append(self.deck.pop())
            #print(len(self.community_cards))
            #print(len(self.deck))
            #print(len(self.opp_hand))
            #Card.print_pretty_cards(self.hand)
            #Card.print_pretty_cards(self.opp_hand)
            #Card.print_pretty_cards(self.community_cards)
            reward = evaluator.evaluate(self.hand,self.community_cards) - evaluator.evaluate(self.opp_hand,self.community_cards)
            self.backpropagate(signe(reward))
            self.current='end'
            self.reward = signe(reward)
        elif self.current == 'end':
            self.backpropagate(self.reward)

            print('JL a tort')






    def playbis(self, depth=0):##a completer
        if depth > 50:  # Limite de récursion pour éviter l'erreur maximum recursion depth exceeded
            return

        if self.current == 'preflop':
            # Gestion du préflop
            if not self.hand:  # Si aucune main n'est définie, générer une main aléatoire.
                self.hand = [(random.randint(2, 14), random.choice('cdhs')), (random.randint(2, 14), random.choice('cdhs'))]
            action = random.choice(['raise', 'call', 'fold'])
            self.preflop_moves = action
            if action == 'fold':
                self.backpropagate(False)  # Simule une perte si le joueur se couche.
                return
            self.current = 'flop'  # Transition vers le flop.

        elif self.current == 'flop':
            # Gestion du flop
            if not self.community_cards:
                # Tirage de trois cartes pour le flop.
                self.community_cards = [(random.randint(2, 14), random.choice('cdhs')) for _ in range(3)]
            action = random.choice(['raise', 'call', 'fold'])
            self.flop_moves = action
            if action == 'fold':
                self.backpropagate(False)
                return
            self.current = 'turn'

        elif self.current == 'turn':
            # Gestion du turn
            if not self.turn_card:
                self.turn_card = [(random.randint(2, 14), random.choice('cdhs'))]
            action = random.choice(['raise', 'call', 'fold'])
            self.turn_moves = action
            if action == 'fold':
                self.backpropagate(False)
                return
            self.current = 'river'

        elif self.current == 'river':
            # Gestion de la river
            if not self.river_card:
                self.river_card = [(random.randint(2, 14), random.choice('cdhs'))]
            action = random.choice(['raise', 'call', 'fold'])
            self.river_moves = action
            if action == 'fold':
                self.backpropagate(False)
                return
            self.current = 'showdown'

        elif self.current == 'showdown':
            # Gestion du showdown, évaluer la main
            self.evaluate_hand()
            self.current = 'end'

        else:
            print('Game Over')

        # Récurse dans les enfants s'il y a une continuation du jeu.
        for child in self.childNodes:
            child.playbis(depth + 1)


def add_nodes_edges(G, node, pos, x_increment=32, y_increment=1, current_depth=0):
    y = -current_depth
    pos[node] = (pos[node][0], y)
    current_depth += 1
    dico = {'fold':0, 'check': -1 , 'raise' : 1}
    for child in node.childNodes:
        
        pos[child] = (pos[node][0] + dico.get(child.find_move())*x_increment, y - y_increment)
        G.add_edge(node, child)
        add_nodes_edges(G, child, pos, x_increment/2, y_increment, current_depth)
        
        
    

# Function to draw the tree with wins and visits information
def draw_tree(root):
    G = nx.DiGraph()
    G.add_node(root)
    pos = {root: (0, 0)}
    add_nodes_edges(G, root, pos)
    wins = {node: f'{node.find_move()}\n  Wins: {node.wins}\nVisits: {node.visits}' for node in G.nodes()}
    nx.draw(G, pos, labels=wins, with_labels=True, node_size=500, node_color='skyblue', font_size=7)
    plt.show()


n=Node()
Node.__init__(n)
n.hand = ['5d','Ac']
n.hand = [Card.new(n.hand[0]),Card.new(n.hand[1])]
n.deck.remove(n.hand[0])
n.deck.remove(n.hand[1])
n.opp_hand=[0,0]
start_time = time.time()
for i in range(2000):
    n.play()
end_time = time.time()
print(end_time-start_time)
Card.print_pretty_cards(n.hand)
draw_tree(n)



def main():


    n=Node()
    Node.__init__(n)
    #res = np.array(0,0)
    start_time = time.time()
    for i in range(10):
        n.play()
    end_time = time.time()
    print(f"temps d'execution: {end_time - start_time} secondes")
    count=0
    for child in n.childNodes:
        print(child.__repr__())
        for grandchild in child.childNodes:

            print(grandchild.__repr__())
        count+=1
        print(count)
    #n.play()
    print(n.__repr__()) ##il faudrait definir la fonction __repr__ pour afficher correctement les informations
    draw_tree(n)


    n=Node()
    Node.__init__(n)
    n.current = 'river'
    n.hand.append(n.deck.pop())
    n.hand.append(n.deck.pop())
    n.opp_hand.append(n.deck.pop())
    n.opp_hand.append(n.deck.pop())

    card1 = n.deck.pop()
    card2 = n.deck.pop()
    card3 = n.deck.pop()
    n.flop_cards = [card1, card2, card3]
    n.community_cards = [card1, card2, card3]
    n.turn_card.append(n.deck.pop())
    n.community_cards.append(n.turn_card)
    n.river_card.append(n.deck.pop())
    n.community_cards.append(n.river_card)


    time_list=[]
    node_list=[]
    sizes = [10, 100,500, 1000, 2000, 5000, 10000, 50000, 100000]
    for N in sizes:

        n=Node()
        Node.__init__(n)
        start_time = time.time()
        for i in range(N):
            n.play()
        end_time = time.time()
        time_list.append(end_time-start_time)
        node_list.append(n)

            
        #Card.print_pretty_cards(n.hand)
        #print(n.__repr__())
        #draw_tree(n)
            #print(Card.print_pretty_cards(n.hand))
    times = time_list


    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, marker='o', color='blue', linestyle='-')
    plt.scatter(sizes, times, color='blue')
    plt.xscale('log')  # Log scale for x-axis
    plt.xlabel('Size', fontsize=14)
    plt.ylabel('Time (seconds)', fontsize=14)
    plt.title('Scatter Plot of Time vs. Size', fontsize=16)
    plt.grid(True)
    plt.show()

    


def check_Addchild():

    n = Node()
    Node.__init__(n)
    s1 = Node()
    s2 = Node()
    s3 = Node()
    s1.preflop_moves='fold'
    s2.preflop_moves = 'fold'
    s3.preflop_moves = 'check'
    n.AddChild(s1)
    n.AddChild(s2)
    n.AddChild(s3)
    for child in n.childNodes:
        print(child.preflop_moves)





