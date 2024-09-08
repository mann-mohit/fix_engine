#include <iostream>
#include "pugixml.hpp"

class TagsParser
{
private:
    struct TagDataStruct
    {
        int             tagNum;
        std::string     tagName;
        std::string     type;
    };

public:
	TagsParser(const std::string xmlPath);

    ~TagsParser();

	void Init();

	bool IsCurrNodeValid() const;

	const pugi::xml_node& GetCurrNode() const;

	void Next();

	void Previous();

	int GetTagNum() const;

    int GetTagNum(const pugi::xml_node& node) const;

	std::string GetTagName() const;

    std::string GetTagName(const pugi::xml_node& node) const;

	std::string GetType() const;

    std::string GetType(const pugi::xml_node& node) const;

    TagsParser::TagDataStruct GetFullTagData() const;

private:
    std::string         m_xmlPath;
    pugi::xml_document  m_xmlDocument;
    pugi::xml_node      m_currNode;
};
