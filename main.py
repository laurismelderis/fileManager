import time

from pathlib import Path
from pathlib import WindowsPath

# A class which holds a required folder name and it's extensions
# that are valid to this folder
class RequiredFolder:
	def __init__(self, name, extenstions):
		self.name = name;
		self.extenstions = extenstions;

	# Checks whether the extension is valid to the folder
	def contains(self, extenstion):
		return extenstion in self.extenstions

# Checks whether the item is folder
def isFolder(item):
	return item.__str__().find('.') == -1;

# Gets file extension
def getExtension(file):
	if isFolder(file):
		return;
	file = file.__str__();
	if file.find('.') != -1:
		pos = file.rfind('.')
		return file[(pos+1):];

# Converts the pathlib.Path().iterdir()list
# to normal string array 
def pathlibListToStrArray(p):
	arr = []
	for i in range(len(p)):
		arr.append(p[i].__str__())
	return arr

def manageFiles():
	# Define what folders with whom extensions you want
	requiredFolders = {
		RequiredFolder('Archives', ['zip', 'rar']),
		RequiredFolder('Discs', ['iso']),
		RequiredFolder('Documents', [
			'doc', 'docx', 'ppt', 'pptx', 'ods',
			'xls', 'xlsx', 'txt', 'rtf' 
		]),
		RequiredFolder('Installation', ['exe', 'msi']),
		RequiredFolder('PDF', ['pdf']),
		RequiredFolder('Torrent', ['torrent'])
	}

	# Get current path
	# Real target path = 'C:/', 'Users', 'laurism', 'Downloads'
	# Test target path = 
	targetPath = WindowsPath('E:/', 'Programming', 'python', 'folder_manager')

	# print(targetPath)

	# Get current directories files and folders
	p = list(Path('.').iterdir())
	pStr = pathlibListToStrArray(p)

	# Check whether the folder has required folders
	for folder in requiredFolders:
		found = folder.name in pStr
		if not found:
			Path.mkdir(targetPath / folder.name, parents=True, exist_ok=True)

	# Move all the files to speciefied directories
	for path in p:
		if not isFolder(path):
			found = False
			ext = getExtension(path);
			for rFolder in requiredFolders:
				if rFolder.contains(ext):
					prevPath = targetPath / path
					newPath = targetPath / rFolder.name / path
					Path(prevPath).rename(newPath);
					found = True
					break
			if not found:
				Path(targetPath / path).rename(targetPath / 'Other' / path);

while True:
	manageFiles()
	time.sleep(3)