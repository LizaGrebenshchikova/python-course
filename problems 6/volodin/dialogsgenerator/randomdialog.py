#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import random

class RandomDialog(object):
    
    def __init__(self, agents, max_len=10):
        self.agents = agents
        self.max_len = max_len

    def generate(self):
        """
        Генерирует случайный диалог состоящий из 1-max_len цепочек.
        При генерации вызывает функцию turn.
        Возвращаемый объект является генератором.
        """
        
        return (yield from list(map(lambda x: self.turn(), range(self.max_len))))
        
    def turn(self):
        """
        Генерирует одну случайную цепочку следующим образом: выбирается случайный агент.
        Он "говорит" случайное сообщение (msg) из своей Agent.kb (используйте next или send(None)).
        (правила того, как выбирать никак не регулируются, вы можете выбирать случайный твит из Agent.kb никак не учитывая
        переданное msg).
        Это сообщение передается с помощью send (помним, что агент - это объект-генератор).
        Далее получаем ответ от всех агентов и возвращаем (генерируем) их (включая исходное сообщение).
        Возвращаемый объект является генератором.
        """
        
        #Почему возвращаемый объект -- генератор, если ответы уже получены? Что генерировать?
        
        agent = random.choice(self.agents)
        agents = self.agents.copy()
        agents.remove(agent)
        firstMsg = agent.send(None)
        
        return [agent.name + " : " + firstMsg] + list(map(lambda x: agent.name + " : " + agent.send(firstMsg), agents))

    def eval(self, dialog=None):
        """
        Превращает генератор случайного далога (который возвращается в self.generate())
        в список списков (пример использования далее).
        Возвращаемый объект является списком.
        """
        if dialog is None:
            dialog = self.generate()
        
        return list(map(lambda x: next(dialog), range(self.max_len)))
            
    def write(self, dialog=None, target=sys.stdout):
        """
        Записывает результат self.eval() в соответствующий поток.
        """
        if dialog is None:
            dialog = self.eval()
        
        def printInFile(msgs):
            target.write('turn {0}\n'.format(msgs[1]))
            target.write("\n".join(msgs[0]))
            target.write('\n\n')
        
        list(map(printInFile, zip(dialog, range(len(dialog)))))
