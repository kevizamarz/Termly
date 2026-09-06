from .knowledge_model import Knowledge

KNOWLEDGE = [
	Knowledge(
		intent="change_directory",
		phrases= [
			"open folder",
			"go to directory",
			"access folder",
			],
		keywords= [
			"open","go", "access", "directory", "folder",
			],
		command= "cd",
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
		keywords= [
			"list", "show", "files", "directory", "folder", "contents",
			],
		command= "ls",
		description= "Lists all the files",
		example= "ls",
	),


]
