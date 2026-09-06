from termly.knowledge_model import Knowledge

def test_knowledge_creation():
	knowledge = Knowledge(
		intent = "list_directory",
		phrases = ["list files", "show files"],
		command="ls",
		description="list files and driectories",
		example="ls"
	)

	assert knowledge.intent == "list_directory"
	assert "list files" in knowledge.phrases
	assert knowledge.command == "ls" 
