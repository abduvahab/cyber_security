# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    my_eception.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: areheman <areheman@student.42mulhouse.fr>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/24 13:20:19 by areheman          #+#    #+#              #
#    Updated: 2023/05/25 14:37:11 by areheman         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #




class my_eception(Exception):

	def __init__(self, err):
		super().__init__()
		self.err = err

	def __str__(self):
		return ("{}".format(self.err))
