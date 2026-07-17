#!/usr/bin/env ruby

require "json"
require "pathname"
require "rexml/document"
require "uri"

site_root = Pathname.new(__dir__)
repository_root = site_root.parent
pages = %w[index.html support.html privacy-policy.html].map { |name| site_root.join(name) }
pages << repository_root.join("index.html")
errors = []

pages.each do |page|
  html = page.read
  relative_name = page.relative_path_from(repository_root)

  ids = html.scan(/\sid="([^"]+)"/).flatten
  id_counts = ids.each_with_object(Hash.new(0)) { |id, counts| counts[id] += 1 }
  id_counts.each do |id, count|
    errors << "#{relative_name}: duplicate id ##{id}" if count > 1
  end

  html.scan(/<img\b[^>]*>/i).each do |tag|
    errors << "#{relative_name}: image is missing alt text: #{tag}" unless tag.match?(/\salt="[^"]*"/i)
  end

  html.scan(%r{<script type="application/ld\+json">(.*?)</script>}m).each_with_index do |match, index|
    JSON.parse(match.first)
  rescue JSON::ParserError => error
    errors << "#{relative_name}: invalid JSON-LD block #{index + 1}: #{error.message}"
  end

  html.scan(/\b(?:href|src)="([^"]+)"/).flatten.each do |reference|
    next if reference.start_with?("http://", "https://", "mailto:", "tel:", "data:")

    path_text, fragment = reference.split("#", 2)
    path_text = URI::DEFAULT_PARSER.unescape(path_text)
    if path_text.empty?
      errors << "#{relative_name}: missing anchor ##{fragment}" if fragment && !ids.include?(fragment)
      next
    end

    target = if path_text.start_with?("/")
               repository_root.join(path_text.delete_prefix("/"))
             else
               page.dirname.join(path_text)
             end.cleanpath
    target = target.join("index.html") if target.directory?

    errors << "#{relative_name}: missing local target #{reference}" unless target.exist?
  end
end

%w[sitemap.xml].each do |name|
  path = site_root.join(name)
  begin
    REXML::Document.new(path.read)
  rescue REXML::ParseException => error
    errors << "#{path.relative_path_from(repository_root)}: invalid XML: #{error.message}"
  end
end

if errors.empty?
  puts "Validated #{pages.length} product and catalog pages, local links, images, anchors, JSON-LD, and sitemap XML."
else
  warn errors.join("\n")
  exit 1
end
