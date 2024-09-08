import sys
import os
import subprocess
import xml.etree.ElementTree as ET

env = os.environ

isAllPackage = False
fixEngineHome = os.environ.get('FIX_ENGINE_HOME')
depDir = os.environ.get('DEP_DIR')

def getLibs(configFile, libDep, action):
    tree = ET.parse(configFile)
    root = tree.getroot()

    allLibs = ''
    if libDep is None:
        return allLibs

    for packageName in libDep.split(' '):
        package = root.find(f'packages/package[@name="{packageName}"]')

        objectType = package.find('objectType').text
        libType = package.find('libType').text
        target = package.find('target').text

        allLibs += ' -L$(TARGET_DIR)/../' + target + ' -l' + target
        generateMakefile(configFile, packageName, action)

    return allLibs

def generateMakefile(configFile, packageName, action):
    global isAllPackage

    tree = ET.parse(configFile)
    root = tree.getroot()

    # Extract basic configuration
    basicConfig = root.find('basicConfig')
    compiler = basicConfig.find('compiler').text
    flags = basicConfig.find('flags').text
    commonIncludeDir = basicConfig.find('commonIncludeDir').text

    # Extract package details
    for package in root.find('packages').findall('package'):
        if isAllPackage == True:
            packageName = package.get('name')

        if packageName == package.get('name'):
            if packageName == 'all':
                packageName = package.get('name')

            objectType = package.find('objectType').text
            libType = package.find('libType').text
            depends = package.find('depends').text
            includeDir = package.find('includeDir').text
            libDep = package.find('libDep').text
            target = package.find('target').text
            targetDir = 'target/' + target

            try:
                os.mkdir(targetDir)
            except OSError as error:
                print(error)

            depFilename = depDir + '/' + packageName + '.dep'
            if 'dep_file' not in depends:
                depends = depends.replace(' ', '\n') + '\n'

                depFile = open(depFilename, 'w')
                depFile.write(depends)
                depFile.close()

            allIncludes = '-I$(FIX_HOME)' + '/' + commonIncludeDir
            if includeDir is not None:
                for dir in includeDir.split(' '):
                    if dir is not None:
                        allIncludes += ' ' + '-I$(FIX_HOME)' + '/' + dir

            allLibs = getLibs(configFile, libDep, action)

            makefileData = f'''\
FIX_HOME = {fixEngineHome}

CXX = {compiler}
CXXFLAGS = {flags} {allIncludes}

TARGET_DIR = $(FIX_HOME)/{targetDir}

SRC_FILE = {depFilename}
SRC = $(shell cat $(SRC_FILE))
OBJ = $(patsubst %.cpp, $(TARGET_DIR)/%.o, $(notdir $(SRC)))

'''

            makefileData += f'''\
STATIC_LIB = $(TARGET_DIR)/lib{target}.a
SHARED_LIB = $(TARGET_DIR)/lib{target}.so
EXE = $(TARGET_DIR)/{target}.exe

'''
            if objectType == 'static_lib':
                dependencyToAdd = '$(STATIC_LIB)'
            elif objectType == 'shared_lib':
                dependencyToAdd = '$(SHARED_LIB)'
            elif objectType == 'exe':
                dependencyToAdd = '$(EXE)'
            else:
                print(f'Invalid objectType for package')
                continue

            makefileData += f'''\
all: $(TARGET_DIR) {dependencyToAdd}

$(TARGET_DIR):
\t mkdir -p $(TARGET_DIR)

$(STATIC_LIB): $(OBJ)
\tar rcs $(STATIC_LIB) $(OBJ)

$(SHARED_LIB): $(OBJ)
\t$(CXX) -shared -o $(SHARED_LIB) $(OBJ)

$(EXE): $(OBJ)
\t$(CXX) $(CXXFLAGS) $(OBJ) {allLibs} -o $(EXE)

'''

            with open(depFilename) as depFile:
                for file in depFile:
                    file = file.replace('\n', '')
                    objFilename = os.path.basename(file.replace('.cpp', '.o'))
                    makefileData += f'''\
$(TARGET_DIR)/{objFilename}: $(FIX_HOME)/{file}
\t$(CXX) $(CXXFLAGS) -c $< -o $@

'''

            makefileData += f'''\
clean:
\t rm -f $(TARGET_DIR)/*.o $(TARGET_DIR)/*.a $(TARGET_DIR)/*.so $(TARGET_DIR)/*.exe
'''

            makefileName = targetDir + '/' + target + '_Makefile'
            makeFile = open(makefileName, 'w')
            makeFile.write(makefileData)
            makeFile.close()

            runMake(makefileName, action)

            if isAllPackage == True:
                continue
            else:
                break

    else:
        print(f'Package {packageName} not found')
        return 2

def runMake(makefileName, action):
    file = f'{makefileName}'
    command = ['/usr/bin/make', '-f', file, action]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(result)
    except OSError as error:
        print(error)

def main():
    global isAllPackage
    allArgs = sys.argv[1:]
    print(allArgs)
    if len(allArgs) != 2:
        print('Usage error')
        return 1

    packageName = allArgs[0]
    if packageName == 'all':
        isAllPackage = True

    action = allArgs[1]

    os.chdir('/home/repos/fix_engine')
    errorCode = generateMakefile('config/MakeConfig.xml', packageName, action)

if __name__ == '__main__':
    exit(main())
