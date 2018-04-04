#!/usr/bin/env ruby

require 'csv'
require 'nokogiri'

if (ARGV.length < 2)
  puts "usage: ruby #{__FILE__} API_HTML_FILE CSV_OUT"
  exit
end

api_dom_path = ARGV[0]
csv_out = ARGV[1]

doc = File.open(api_dom_path) { |f| Nokogiri::HTML(f) }

CSV.open(csv_out, "wb") do |csv|
  csv << ["full_name", "type", "descname"]
  doc.css("dl[@class='function']>dt").each do |definition|
    full_name = definition['id']
    parts = full_name.split(".")
    descname = parts.pop
    type = parts.pop
    csv << [ full_name, type, descname ]
  end
end