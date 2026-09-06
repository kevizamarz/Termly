from .knowledge_model import Knowledge

KNOWLEDGE = [
	Knowledge(
		intent="change_directory",
		phrases= [
			"open downloads",
			"go to downloads",
			"access downloads",
			],
		command= "cd Downloads",
		description= "Moves you into the Downloads folder",
		example= "cd Downloads",
	),

	Knowledge(
		intent="list_directories",
		phrases= [
			"list files",
			"show files",
			"show directory contents",
			],
		command= "ls",
		description= "Lists all the files",
		example= "ls",
	),


]
