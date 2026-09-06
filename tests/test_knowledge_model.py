from termly.knowledge_model import Knowledge

def test_knowledge_creation():
	knowledge = Knowledge(
		intent = "list_directory",
		phrases = ["list files", "show files"],
		keywords= ["list", "show", "files", "directory"],
		command="ls",
		description="list files and driectories",
		example="ls"
	)

	assert knowledge.intent == "list_directory"
	assert "list files" in knowledge.phrases
	assert knowledge.command == "ls" 
	assert "files" in knowledge.keywords
