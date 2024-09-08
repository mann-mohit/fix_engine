#include "TagsParser.h"

TagsParser::TagsParser(const std::string xmlPath) :
    m_xmlPath(xmlPath)
{
   
}

TagsParser::~TagsParser()
{
}

void TagsParser::Init()
{
    m_xmlDocument.load_file(m_xmlPath.c_str());
    m_currNode = m_xmlDocument.first_child().first_child();
}

bool TagsParser::IsCurrNodeValid() const
{
    return m_currNode != NULL;
}

const pugi::xml_node& TagsParser::GetCurrNode() const
{
    return m_currNode;
}

void TagsParser::Next()
{
    m_currNode = m_currNode.next_sibling();
}

void TagsParser::Previous()
{
    m_currNode = m_currNode.previous_sibling();
}

int TagsParser::GetTagNum() const
{
    pugi::xml_attribute attr = m_currNode.attribute("tagNum");
    return atoi(attr.value());
}

int TagsParser::GetTagNum(const pugi::xml_node& node) const
{
    pugi::xml_attribute attr = node.attribute("tagNum");
    return atoi(attr.value());
}

std::string TagsParser::GetTagName() const
{
    pugi::xml_attribute attr = m_currNode.attribute("tagName");
    return attr.value();
}

std::string TagsParser::GetTagName(const pugi::xml_node& node) const
{
    pugi::xml_attribute attr = node.attribute("tagName");
    return attr.value();
}

std::string TagsParser::GetType() const
{
    pugi::xml_attribute attr = m_currNode.attribute("type");
    return attr.value();
}

std::string TagsParser::GetType(const pugi::xml_node& node) const
{
    pugi::xml_attribute attr = m_currNode.attribute("type");
    return node.value();
}

TagsParser::TagDataStruct TagsParser::GetFullTagData() const
{
    TagsParser::TagDataStruct data;
    data.tagNum = GetTagNum();
    data.tagName = GetTagName();
    data.type = GetType();

    return data;
}
