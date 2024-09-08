#include "TagsParser.h"

using namespace std;

int main(int argc, char *argv[])
{
	TagsParser tagsParser("/home/repos/fix/config/Tags.xml");

	tagsParser.Init();

	while (tagsParser.IsCurrNodeValid())
	{
		cout << tagsParser.GetTagNum() << "\n";
		tagsParser.Next();
	}
}
