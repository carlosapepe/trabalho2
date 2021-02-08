#!/usr/bin/python
# This Python file uses the following encoding: utf-8

## -------------------------------------------------------------------------------
## -------------------------------------------------------------------------------
# Criado por Carlos Alberto Pedroso
# Data: 07/02/2021
# Para disciplina de Otimização (trabalho 2)
# Professor André Guedes 
## -------------------------------------------------------------------------------
## -------------------------------------------------------------------------------

import classes
import timeit
import sys
# import numpy as np
#def configVariables():
#    global n_nodes
n_nodes = 0

optV = 0  # custo otimo (inicializar com a soma dos valores de todos os atores)
optX = [] # elenco escolhido

#---------------------------------------------------------------------------------
# Função de leitura do arquivo de entrada e separação dos valores
#---------------------------------------------------------------------------------
def readInput():
    global optV
    first_line = raw_input()
    first_line_list = first_line.split()
    n_group = int(first_line_list[0])
    n_actor = int(first_line_list[1])
    n_character = int(first_line_list[2])
    if n_group <= 0 or n_actor <= 0 or n_character <= 0:
        return [], [], 0, [], 0
    groups_list_id = [i for i in range(1, n_group + 1) ]
    actors_list_id = [i for i in range(1, n_actor + 1) ]
    actors = []
    try:
        for i in range(n_actor):
            actor_line = raw_input()
            actor_line_list = actor_line.split()
            cost = int(actor_line_list[0])
            groups = int(actor_line_list[1])
            if cost < 0 or groups < 0:
                return [], [], 0, [], 0
            actor_groups_list = []
            for j in range(groups):
                group = int(raw_input())
                if group > n_group or group < 0:
                    return [], [], 0, [], 0
                actor_groups_list.append(group)
            actor = classes.Actor(i+1, cost, actor_groups_list)
            actors.append(actor)
            optV+=cost
    except:
        return [], [], 0, [], 0
    return groups_list_id, actors_list_id, n_character, actors, n_group
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Função de verificação de viabilidade da solução encontrada
#---------------------------------------------------------------------------------
def isViable(cast, n_character):
    #print('cast ', cast, 'n_character ',n_character, 'sum_cast ', sum(cast))
    return sum(cast) == n_character 
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
# Função de verificação de inviabilidade da solução encontrada
#---------------------------------------------------------------------------------
def isUnviable(stack_index, next_actors_list, last_index):
    # VERIFICAR
    print('stk f', stack_index == 0)
    print('nxt ', len(next_actors_list) == 0)
    print(stack_index,next_actors_list)
    print(stack_index == last_index) and (len(next_actors_list) == 0)
    return (stack_index == 0) and (len(next_actors_list) == 0) or (stack_index == last_index) and (len(next_actors_list) == 0)
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Função de representatividade da cobertura dos grupos
#---------------------------------------------------------------------------------
def checkGroups(cast, actor, n_group):
    cast_cost = 0
    group_list = [ 0 for i in range(0,n_group) ]
    #print('cast ', cast)
    for ai, data in enumerate(cast):
        # print(data)
        if data == 1:
            # print(data)
            aux = actor[ai]
            actor_group = aux.groups
            cast_cost+=aux.cost
            #print('cast', cast)
            #print('actor list',actor_group)
            for i in actor_group:
                group_list[i-1] = 1
    #print('group list',group_list)
    #print('cast cost ', cast_cost)
    #print('cast ',cast)
    return sum(group_list) == n_group, cast_cost
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------    
  #optV = mean(n_character, actors)
    # aux = [0 for i in range(len(actors))]
    # for i in lower:
    #     ai = i.id
    #     for index, a in enumerate(actors):
    #         if a.id == ai:
    #             aux[index] = 1
    # optX = aux
    # para crescente comente essa linha
    # actors_list_id = [i.id for i in actors]----------------------------------------------------------
# Função checagem
#---------------------------------------------------------------------------------
def checkStack(stack):
    return stack[0], stack[1]
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------  

#---------------------------------------------------------------------------------
# Função de printar o resultado na tela
#---------------------------------------------------------------------------------
def printOutput(x, actors, optV, n_nodes, fim, inicio):
    
    if x:
        aux = []
        for ai, data in enumerate(x):
            if data == 1:
                aux.append(str(actors[ai].id))
        aux = sorted(aux, key=lambda x: x, reverse=False)
        print(' '.join(aux))
        print(optV)

    else:
        print('Inviável')  

    #print('Duração do Programa: %fs' % (fim - inicio))
    sys.stderr.write('Duração do Programa: %fs  \n' %(fim - inicio))
    sys.stderr.write('Numero de nós gerados: {}\n'.format(n_nodes))
    sys.stderr.write('Arvore geradora: {}\n'.format(arvore(actors)))
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------    

#---------------------------------------------------------------------------------
# Função de verificação do tamanho da árvore binária
#---------------------------------------------------------------------------------  
def arvore(actors):
    n = 2
    k = len(actors)
    pot = ((n**k)-1)*2 
        #i   = i + 1
    #print('arvore', pot)
    return pot
#---------------------------------------------------------------------------------
#--------------------------------------------------------------------------------- 

#---------------------------------------------------------------------------------
# Função de corte pelo nível
#---------------------------------------------------------------------------------
def poda(cast,n_actor,n_character,level):
#def bound2(cast,n_character,level):
    #print ('O que falta ', sum(cast) + n_character - level, 'eh menor do que preciso ', n_character)
    #if ((sum(cast) + (n_character - level)) < n_character):
    #if ((sum(cast) + (n_actor - level)) < n_character):
        return ((sum(cast) + (n_actor - level)))
#---------------------------------------------------------------------------------
#--------------------------------------------------------------------------------- 

#---------------------------------------------------------------------------------
# Função de bound 1 onde verifica o custo do cast
#--------------------------------------------------------------------------------- 
def bound1(actor, n_character, cast):
    global optV
    # global optX
    cost = 0
    # print('cast ', cast)
    # print('optV bound ', optV)
    for i, data in enumerate(cast):
        if data:
            cost += actor[i].cost
    #return cost < optV
    return cost
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Função de bound 2 o que tenho na mão e o próximo elemento para cortar
#--------------------------------------------------------------------------------- 
def bound3(cast,actor,n_group, level,n_character):
    allgroups, cast_cost = checkGroups(cast, actor, n_group)
    if level < n_character and actor[level].cost >= cast_cost:
        return cast_cost + actor[level].cost 
    return cast_cost 
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Função de branch 2 o que tenho na mão e o próximo elemento para não descer
#--------------------------------------------------------------------------------- 
def branch3(cast, level, n_character, n_actor, actor, n_group):

    global n_nodes
    global optV
    global optX

    if poda(cast,n_actor,n_character,level) < n_character:
        return
    elif level < n_character:
        bound = bound3(cast,actor,n_group, level,n_character)
        # print(bound)
        if bound > optV:
            return
    if isViable(cast, n_character):
        allgroups, cast_cost = checkGroups(cast, actor, n_group)
        allgroupsOpt, opt_cost = checkGroups(optX, actor, n_group)
        if allgroups:
            if not allgroupsOpt:
                optX = cast
                optV = cast_cost
            elif cast_cost < optV:
               optV = cast_cost
               optX = cast
        return
    
    #1
    #bound = bound3(cast,actor,n_group, level,n_character)
    aux = cast[:]
    if len(aux) < n_actor: #and bound < optV:
        aux.append(1)
        n_nodes+=1
        branch3(aux, level + 1, n_character, n_actor, actor, n_group) 

    #0
    #bound = bound3(cast,actor,n_group, level,n_character)
    aux = cast[:]
    if len(aux) < n_actor: #and bound < optV:
        aux.append(0)
        n_nodes+=1
        branch3(aux, level + 1, n_character, n_actor, actor, n_group)

    if level == n_actor + 1:
        return 
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Função de branch 1 faz a verificação pelo custo do cast na mão
#--------------------------------------------------------------------------------
def branch1(cast, level, n_character, n_actor, actor, n_group):

    global n_nodes
    global optV
    global optX

    if poda(cast,n_actor,n_character,level) < n_character:
        return
    # elif level < n_character:
    #     bound = bound1(actor, n_character, cast)
    #     # print(bound)
    #     if bound > optV:
    #         return
    #if poda(cast,n_actor,n_character,level) < n_character:
        #return
    # print('custo bound {} no nivel {} e optv {} e optx{}'.format(bound(actor, n_character, cast),level,optV,optX))
    # print('level {} '.format(level), 'n_nodes {} '.format(n_nodes), cast) 
    # print('n_character ',n_character, 'cast ', cast)   
    if isViable(cast, n_character):
        #print('Cast ', cast)
        # print('Solução viável {} no level {}'.format(cast, level))
        allgroups, cast_cost = checkGroups(cast, actor, n_group)
        allgroupsOpt, opt_cost = checkGroups(optX, actor, n_group)
        if allgroups:
            # print('Solução viável {} no level {}'.format(cast, level))
            # print('Solução viável {} no level {} - cost {}'.format(cast, level,cast_cost))
            if not allgroupsOpt:
                optX = cast
                optV = cast_cost
            elif cast_cost < optV:
               optV = cast_cost
               optX = cast
        # calcula bound
        # compara bound com o optv
        # se verdade dá return senão continua
        return
    # 1
    bound = bound1(actor, n_character, cast)
    aux = cast[:]
    if len(aux) < n_actor and bound < optV:
        aux.append(1)
        n_nodes+=1
        branch1(aux, level + 1, n_character, n_actor, actor, n_group) 
    
    # 0
    bound = bound1(actor, n_character, cast)
    aux = cast[:]
    if len(aux) < n_actor and bound < optV:
        aux.append(0)
        n_nodes+=1
        branch1(aux, level + 1, n_character, n_actor, actor, n_group) 

    if level == n_actor + 1:
        return 
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Função de ordenação e média para incializar o optV
#--------------------------------------------------------------------------------
def mean(n_character, actors):
    sort = sorted(actors, key=lambda x: x.cost, reverse=False)
    lower = sort[:n_character]  
    sum_lower = sum(l.cost for l in lower)
    upper = sort[len(actors) - n_character:]  
    sum_upper = sum(l.cost for l in upper)
    # print(sum_lower,sum_upper, sum_lower + (sum_lower + sum_upper)/2,(sum_lower + sum_upper)/2)
    return sum_lower + (sum_lower + sum_upper)/2
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Função de ordenação e média para incializar o optV
#--------------------------------------------------------------------------------
def main(argc, argv):
    
    global optV
    global optX
    groups_list_id, actors_list_id, n_character, actors, n_group = readInput()
    #optV = mean(n_character, actors)
    # aux = [0 for i in range(len(actors))]
    # for i in lower:
    #     ai = i.id
    #     for index, a in enumerate(actors):
    #         if a.id == ai:
    #             aux[index] = 1
    # optX = aux
    # para crescente comente essa linha
    # actors_list_id = [i.id for i in actors]
    if len(actors) < n_character:
        print('Inviável')
        return
    elif len(groups_list_id) == 0 or len(actors_list_id) == 0 or n_character == 0 or len(actors) == 0:
        # sera que coloco inviavel?
        print('Erro na leitura do arquivo')
        return

    level = 0
    # cast = [0 for i in actors]
    cast=[]
    #nodes = 0
    global n_nodes
    inicio = timeit.default_timer()
    if argc > 1:
        # print(argv)
        if argv[1] == '-a':
            branch3(cast, level, n_character, len(actors), actors, n_group)
        #elif argv[1] == '-b':
            #branch2(cast, level, n_character, len(actors), actors, n_group)
    else:
        branch1(cast, level, n_character, len(actors), actors, n_group)
    fim = timeit.default_timer()
    printOutput(optX, actors, optV, n_nodes, fim, inicio)
    #print(n_nodes)
    #print('menor custo ', optV, optX)
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------