import numpy as np
import matplotlib.pyplot as plt

# regarder les point de départ et d'arriver et executer la fonction du graph
# regarder la trajectory pour la liste des arrival times [-1] - [0]

def figure_4(T_t,T_d, C_t,C_d, I_t,I_d, T_d_inf,C_d_inf,I_d_inf,save_path= "results"):
	# T, C, I : Transit(no carpooling), Carpooling only, Integrated
	# _t : time in minutes
	# _d : distance in km
	# _inf : with infinite time (unserved riders)
	T_t,T_d, C_t,C_d, I_t,I_d, T_d_inf,C_d_inf,I_d_inf = np.array(T_t),np.array(T_d), np.array(C_t),np.array(C_d), np.array(I_t),np.array(I_d), np.array(T_d_inf),np.array(C_d_inf),np.array(I_d_inf)
	def set_share_axes(axs, target=None, sharex=False, sharey=False):
		if target is None:
			target = axs.flat[0]
		# Manage share using grouper objects
		for ax in axs.flat:
			from pprint import pprint
			pprint(vars(target.xaxis))
			print("type of target = ",type(target))
			if sharex:
				target._sharex = True
			if sharey:
				target._sharey =True
		# Turn off x tick labels and offset text for all but the bottom row
		if sharex and axs.ndim > 1:
			for ax in axs[:-1,:].flat:
				ax.xaxis.set_tick_params(which='both', labelbottom=False, labeltop=False)
				ax.xaxis.offsetText.set_visible(False)
		# Turn off y tick labels and offset text for all but the left most column
		if sharey and axs.ndim > 1:
			for ax in axs[:,1:].flat:
				ax.yaxis.set_tick_params(which='both', labelleft=False, labelright=False)
				ax.yaxis.offsetText.set_visible(False)

	fig, axs = plt.subplots(nrows=2, ncols=3, gridspec_kw={'height_ratios': [1, 2]}) # 'width_ratios'

	set_share_axes(axs[0,:], sharey=True)
	set_share_axes(axs[1,:], sharex='row', sharey='col')

	#fig.suptitle('Systems comparison',fontsize = 20)
	NUMBER_OF_BARS = 7
	#plt.xlabel("km")
	#plt.ylabel("minutes")

	vector_bar = np.linspace(2,int(np.max([np.max(T_d),np.max(C_d),np.max(I_d)])),NUMBER_OF_BARS*2).reshape(-1,2)
	list_bar = [len(list(filter(lambda x : i<x<=j, I_d_inf))) for i,j in vector_bar]
	axs[0,0].bar(list(map(lambda x : str(np.round(x,1)),vector_bar)),list_bar,color='0.0')
	axs[1,0].scatter(I_d, I_t,color='0.0',s=1.75)
	line_x = np.linspace(0,np.max([np.max(T_d),np.max(C_d),np.max(I_d)]))
	line_y = np.clip(line_x*60/4.5,0,np.max([np.max(T_t),np.max(C_t),np.max(I_t)]))
	axs[1,0].plot(line_x, line_y,color='gray',alpha=0.25)
	axs[1,0].fill_between(line_x, line_y, 0, color='1.0', alpha=.1)
	axs[1,0].fill_between(line_x, line_y, np.max([np.max(T_t),np.max(C_t),np.max(I_t)]), color='1.0', alpha=.1)
	axs[0,0].set_xticklabels(list(map(lambda x : str(int(x[0]))+"-"+str(int(x[1])),vector_bar)),fontsize=10/int(NUMBER_OF_BARS/5))

	axs[1,0].set_xlabel("Distance between origin and destination (km)")
	axs[1,0].set_ylabel("Travel time (minutes)")
	axs[0,0].set_xlabel("Interval of distances between origin and destination (km)")
	axs[0,0].set_ylabel("Number of riders unserved")

	axs[1,0].grid()
	axs[0,0].set_title('No carpooling system',fontsize = 20)

	vector_bar = np.linspace(2,int(np.max([np.max(T_d),np.max(C_d),np.max(I_d)])),NUMBER_OF_BARS*2).reshape(-1,2)
	list_bar = [len(list(filter(lambda x : i<x<=j, C_d_inf))) for i,j in vector_bar]
	axs[0,1].bar(list(map(lambda x : str(np.round(x,1)),vector_bar)),list_bar,color='0.0')
	axs[1,1].scatter(C_d, C_t,color='0.0',s=1.75)
	line_x = np.linspace(0,np.max([np.max(T_d),np.max(C_d),np.max(I_d)]))
	line_y = np.clip(line_x*60/4.5,0,np.max([np.max(T_t),np.max(C_t),np.max(I_t)]))
	axs[1,1].plot(line_x, line_y,color='gray',alpha=0.25)
	axs[1,1].fill_between(line_x, line_y, 0, color='1.0', alpha=.1)
	axs[1,1].fill_between(line_x, line_y, np.max([np.max(T_t),np.max(C_t),np.max(I_t)]), color='1.0', alpha=.1)
	axs[0,1].set_xticklabels(list(map(lambda x : str(int(x[0]))+"-"+str(int(x[1])),vector_bar)),fontsize=10/int(NUMBER_OF_BARS/5))

	axs[1,1].grid()
	axs[0,1].set_title('Current system',fontsize = 20)

	#axs[0,0].scatter(T_d_inf, np.random.random(len(T_d_inf))*100,color='green',s=1.75) # blue,green,red,purple
	vector_bar = np.linspace(2,int(np.max([np.max(T_d),np.max(C_d),np.max(I_d)])),NUMBER_OF_BARS*2).reshape(-1,2)
	list_bar = [len(list(filter(lambda x : i<x<=j, T_d_inf))) for i,j in vector_bar]
	axs[0,2].bar(list(map(lambda x : str(np.round(x,1)),vector_bar)),list_bar,color='0.0')
	axs[1,2].scatter(T_d, T_t,color='0.0',s=1.75)
	line_x = np.linspace(0,np.max([np.max(T_d),np.max(C_d),np.max(I_d)]))
	line_y = np.clip(line_x*60/4.5,0,np.max([np.max(T_t),np.max(C_t),np.max(I_t)]))
	axs[1,2].plot(line_x, line_y,color='gray',alpha=0.25)
	axs[1,2].fill_between(line_x, line_y, 0, color='1.0', alpha=.1)
	axs[1,2].fill_between(line_x, line_y, np.max([np.max(T_t),np.max(C_t),np.max(I_t)]), color='1.0', alpha=.1)
	axs[0,2].set_xticklabels(list(map(lambda x : str(int(x[0]))+"-"+str(int(x[1])),vector_bar)),fontsize=10/int(NUMBER_OF_BARS/5))

	axs[1,2].grid()
	axs[0,2].set_title('Integrated system',fontsize = 20)

	plt.rc('axes', titlesize=30)     # fontsize of the axes title
	plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
	plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
	#plt.axis("equal")
	if save_path != "":
		print("______________________________________________________________________")
		plt.savefig(save_path+"/system_comparison.eps",format="eps")

	plt.show()

if __name__=="__main__":
	vecteur1 = np.random.random(100)*100
	vecteur2 = np.linspace(1,100,100)
	vecteur3 = np.random.random(50)*100
	figure_4(vecteur1,vecteur2,vecteur1,vecteur2,vecteur1,vecteur2, vecteur3,vecteur3,vecteur3,save_path="")