import random
import networkx as nx
import matplotlib.pyplot as plt
import time 

class node :
    def __init__(self, id):
        self.id = id #int

    def get_id(self):
        return self.id

class arete:
    def __init__(self, cout , duree,start, end):
        self.cout = cout #int
        self.duree = duree #int
        self.start = start #node
        self.end = end #node
        self.lagrange = 0
    
    def __eq__(self, a):
        if isinstance(a,tuple) and len(a)==2:
            start,end = a
            return self.start.id == start and self.end.id == end
        return False

    def test(self,a,b):
        return self.start.id == a and self.end.id == b
        
    
    def get_chemin(self):
        return (self.cout, self.duree, self.start, self.end,self.lagrange)
    
    def get_cout_duree(self):
        return (self.cout,self.duree)
    
    def get_lagrange(self):
        return self.lagrange

    def mono_critere(self, val):
        self.lagrange = val
    

class Graphe:
    def __init__(self):
        self.nodes = [] #nodes type
        self.aretes = [] #arete type

    def add_node(self, node):
        self.nodes.append(node)

    def add_arete(self, arete):
        self.aretes.append(arete)
    
    def calcul_chemin(self, tab):
        cout_total = 0
        duree_total = 0

        for i in range(len(tab)-1):
            for arete in self.aretes:
                if arete.test(tab[i],tab[i+1]):
                    x,y = arete.get_cout_duree()
                    cout_total += x
                    duree_total += y
                    break

        return (cout_total,duree_total)

    def function_lagrange(self, f1, f2, vlambda):
        return f1 + vlambda * f2
    
    def relaxation_probleme(self, vlambda):
        for arete in self.aretes:
            arete.mono_critere(self.function_lagrange(arete.cout,arete.duree,vlambda))


    def generer_graphe(self, nbr_node, nb_cout_max, nb_duree_max):
        #creation des noeuds
        for i in range(nbr_node):
            noeud = node(i)
            self.add_node(noeud)
        
        impair = len(self.nodes) % 2 == 1
        
        if impair is True:
            fin = len(self.nodes) - 1
        else:
            fin = len(self.nodes)

        moitie = int(fin/2)

        #aretes horizontales
        for i in range (moitie-1):
            cout = random.randint(1, nb_cout_max)
            if cout >= nb_cout_max // 2:
                duree = random.randint(1,nb_duree_max//4)
            else :
                duree = random.randint(nb_duree_max//4,nb_duree_max)

            self.add_arete(arete(cout,duree,self.nodes[i], self.nodes[i+1]))
        
        for i in range (moitie, fin-1):
            cout = random.randint(1, nb_cout_max)
            if cout >= nb_cout_max // 2:
                duree = random.randint(1,nb_duree_max//4)
            else :
                duree = random.randint(nb_duree_max//4,nb_duree_max)
            self.add_arete(arete(cout,duree,self.nodes[i], self.nodes[i+1]))

        #aretes verticales
        for i in range (moitie):
            cout = random.randint(1, nb_cout_max)
            if cout >= nb_cout_max // 2:
                duree = random.randint(1,nb_duree_max//4)
            else :
                duree = random.randint(nb_duree_max//4,nb_duree_max)
            self.add_arete(arete(cout,duree,self.nodes[i], self.nodes[i+moitie]))

        #aretes diagonales
        for i in range (moitie-1):
            cout = random.randint(1, nb_cout_max)
            if cout >= nb_cout_max // 2:
                duree = random.randint(1,nb_duree_max//4)
            else :
                duree = random.randint(nb_duree_max//4,nb_duree_max)
            self.add_arete(arete(cout,duree,self.nodes[i], self.nodes[i+moitie+1]))

        for i in range (moitie, fin-1):
            cout = random.randint(1, nb_cout_max)
            if cout >= nb_cout_max // 2:
                duree = random.randint(1,nb_duree_max//4)
            else :
                duree = random.randint(nb_duree_max//4,nb_duree_max)
            self.add_arete(arete(cout,duree,self.nodes[i], self.nodes[(i-moitie)+1]))

        #cas où nombre de noeud impair
        if impair is True:
            cout = random.randint(1, nb_cout_max)
            if cout >= nb_cout_max // 2:
                duree = random.randint(1,nb_duree_max//4)
            else :
                duree = random.randint(nb_duree_max//4,nb_duree_max)
            self.add_arete(arete(cout,duree,self.nodes[moitie-1], self.nodes[len(self.nodes)-1]))

            cout = random.randint(1, nb_cout_max)
            if cout >= nb_cout_max // 2:
                duree = random.randint(1,nb_duree_max//4)
            else :
                duree = random.randint(nb_duree_max//4,nb_duree_max)
            self.add_arete(arete(cout,duree,self.nodes[fin-1], self.nodes[len(self.nodes)-1]))

    
    def afficher_graphe(self):
        print(f"Nombre de noeuds : {len(self.nodes)}")       
        print("\n Arêtes avec coûts et durées :")

        for arete in self.aretes:
            print(f" - {arete.start.id} --> {arete.end.id} : Coût = {arete.cout}, Durée = {arete.duree}")
                 

class Solution:
    def __init__(self, chemin, val_chemin, lagrange_chemin):
        self.chemin = chemin
        self.val_chemin = val_chemin
        self.lagrange_chemin = lagrange_chemin
    
    def __eq__(self, objet):
        if isinstance(objet, list):
            return self.chemin == objet


def relaxation_lagrangienne(graphe,min_c1,min_c2):
    pareto = [min_c1,min_c2]
    solution_parcouru = [] #les solutions parcourues 
    start = min_c1
    end = min_c2
    tab = [] 
    i = 1
    
    while end != start:

        aaa, epsilon = start
        tab.append(start)
        tab.append(end)

        print(f'Itération n°{i} :')

        while True:
            
            #calcul de lambda
            vlambda = recherche_lambda(tab)

            #relaxation du problème
            graphe.relaxation_probleme(vlambda)

            #calcul de la meilleure solution selon le critère de lagrange
            chemin_plus_court = get_chemin_plus_court(graphe,"lagrange")
            val_chemin = graphe.calcul_chemin(chemin_plus_court)
            lagrange_chemin = fonction_lagrange(val_chemin, vlambda, epsilon)

            #test si on trouve la même solution
            if val_chemin in solution_parcouru or val_chemin in tab:

                #test du cas où le tuple qui minimise x est le même que celui qui minimise y 
                if len(solution_parcouru) != 0:
                    solution = max_solution(solution_parcouru)
                    pareto.append(solution.val_chemin)
                    start = solution.val_chemin

                    print('Solutions parcourues :')
                    for zz in solution_parcouru:
                        print(zz.val_chemin, end='')
                    print()

                    tab = []
                    solution_parcouru = []
                    i += 1
                    break
                
                return pareto
            else:
                temp = Solution(chemin_plus_court,val_chemin,lagrange_chemin)
                solution_parcouru.append(temp)
                tab.append(temp.val_chemin)
    
    return pareto

def recherche_lambda(tab):
    temp = []

    for i in range(len(tab)-1):
        for y in range(i+1,len(tab)):
            a,b = tab[i]
            c,d = tab[y]

            if b == d:
                break
            x = (c-a)/(b-d)

            temp.append(x)

    return min(temp) 

def max_solution(tab):
    sol = tab[0]
    val = sol.lagrange_chemin

    for solution in tab:
        if solution.lagrange_chemin > val:
            sol = solution
            val = solution.lagrange_chemin

    return sol

def fonction_lagrange(tuple, vlambda , epsilon):
    fx,gx = tuple
    return fx + vlambda * (gx - epsilon)


def generate_problem(nb_noeud, nb_duree_max, nb_cout_max):
    graphe = Graphe()
    graphe.generer_graphe(nb_noeud, nb_duree_max, nb_cout_max)
    #graphe.afficher_graphe()

    return graphe


def get_chemin_plus_court(graphe, critere):
    G = nx.DiGraph()
    for node in graphe.nodes:
        G.add_node(node.get_id())
    
    for arete in graphe.aretes:
        G.add_edge(
        arete.start.get_id(),
        arete.end.get_id(),
        cout=arete.cout,
        duree=arete.duree,
        lagrange = arete.lagrange
    )

    #calcul du plus court chemin selon un critère
    temp = nx.shortest_path(G, 0, len(graphe.nodes)-1, critere)
    
    return temp

def afficher_frontiere_pareto(tab, titre):
    #tri selon le coût du + petit au + grand
    pareto = sorted(tab, key=lambda p: p[0])
    x, y = zip(*pareto)
    
    for xy in zip(x, y):
        plt.annotate('(%s, %s)' % xy, xy=xy)

    plt.plot(x, y, marker='o') 
    plt.xlabel('cout')
    plt.ylabel('durée')
    plt.title(titre)
    plt.grid(False)
    plt.show(block=False)


def pareto_brut(graphe):
    G = nx.DiGraph()
    for node in graphe.nodes:
        G.add_node(node.get_id())
    
    for arete in graphe.aretes:
        G.add_edge(
        arete.start.get_id(),
        arete.end.get_id(),
        cout=arete.cout,
        duree=arete.duree,
        lagrange = arete.lagrange
    )

    #recuperation de tout les chemins possibles
    tab= list(nx.all_simple_paths(G, 0, len(graphe.nodes)-1))

    solutions = []    

    #calcul de tout les couts et durées totales pour toutes les solutions
    for sol in tab :
        solutions.append(graphe.calcul_chemin(sol))
   
    frontiere_pareto = []

    for i in range(len(solutions)):
        cout_i, duree_i = solutions[i]
        domine = False

        #on test si i est dominé par quelqu'un
        for y in range(len(solutions)):
            if i == y:
                continue
            
            cout_y,duree_y = solutions[y]
            

            #on test si y domine i
            if (cout_y <= cout_i and duree_y < duree_i) or (cout_y < cout_i and duree_y <= duree_i):
                domine = True
                break
        
        if not domine:
            frontiere_pareto.append(solutions[i])
 
    
    return frontiere_pareto

def main(nb_noeud,cout_max,duree_max):
    #génération du problème
   graphe= generate_problem(nb_noeud,cout_max,duree_max)

   #calcul des bornes de la frontière de pareto 
   sol_c1_min = get_chemin_plus_court(graphe,"cout")
   sol_c2_min = get_chemin_plus_court(graphe,"duree")
   c1_min = graphe.calcul_chemin(sol_c1_min)
   c2_min = graphe.calcul_chemin(sol_c2_min)
   

   #calcul avec la relaxation lagrangienne
   start_time = time.time()
   pareto = relaxation_lagrangienne(graphe,c1_min,c2_min)
   end_time = time.time()
   print(f'Temps d exécution de la relaxation lagrangienne : {end_time - start_time} sec')
   print(f"Nombre de solutions avec la relaxation lagrangienne : {len(pareto)}") 
   plt.figure(1)
   afficher_frontiere_pareto(pareto,'Frontière de Pareto avec la relaxation lagrangienne')
   
   #calcul avec brut force
   brut_pareto = pareto_brut(graphe)
   print(f"Nombre de solutions avec brut-force : {len(brut_pareto)}")
   plt.figure(2)
   afficher_frontiere_pareto(brut_pareto,'Frontière de Pareto avec brut force')

   input("Appuyez sur Enter pour fermer les fenêtres...")
    
main(20,20,20)