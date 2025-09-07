import yaml
import xml.etree.ElementTree as xml_tree

# Load YAML data
with open('feed.yaml', 'r', encoding='utf-8') as file:
    yaml_data = yaml.safe_load(file)

# Create RSS element with proper namespaces
rss_element = xml_tree.Element('rss', {
    'version': '2.0',
    'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
})

# Create channel element
channel_element = xml_tree.SubElement(rss_element, 'channel')

link_prefix = yaml_data['link']

# Podcast-level details
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'link').text = link_prefix
xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

# Loop through each episode
for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text = item['title']
    # Use episode author if exists, otherwise use main author
    xml_tree.SubElement(item_element, 'itunes:author').text = item.get('author', yaml_data['author'])
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']

    # Fix length: remove commas if present
    length_value = str(item['length']).replace(',', '')

    xml_tree.SubElement(item_element, 'enclosure', {
        'url': link_prefix + item['file'],
        'type': 'audio/mpeg',
        'length': length_value
    })

# Write to XML file
output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)

print("✅ podcast.xml generated successfully!")
