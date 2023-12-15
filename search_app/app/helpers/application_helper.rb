module ApplicationHelper
    # app/helpers/application_helper.rb
    def render_thumbnail(document, options)
        return unless document[:file_id].present?
        image_tag(
        "#{image_server}/#{document.id}/#{document.first(:file_id)}.png",
        options.merge(alt: presenter(document).document_heading)
        )
    end

    def extract_year_from_date(date_string)
        # Convert the date string to a Ruby DateTime object
        date_time = Date.parse(date_string)
      
        # Extract the year from the DateTime object
        year = date_time.year
      
        # Return the year
        year
    end

    def summarize_summary(document, max_length = 800)
        source_hash = document[:document]._source
        summary = source_hash['summary']
        if summary.length > max_length
            truncated_summary = "#{summary[0, max_length]}..."
            read_more = link_to_page(document)
            "#{truncated_summary} #{read_more}".html_safe
        else
          summary
        end
    end



    def show_date(document)
        source_hash = document[:document]._source
        date_value = source_hash['date']
        format_date(date_value)
    end

    def format_date(date_string)
        date_object = Date.parse(date_string)
        date_object.strftime("%Y-%m-%d")
    end

    # Define a helper method to generate clickable links for any attribute
    def link_to_event(document)
        source_hash = document[:document]._source
        event_value = source_hash['event']
        event_name = source_hash['label']
        link_name = "#{event_name} on Wikidata"
        link_to link_name, event_value, target: '_blank'
    end
      
    def link_to_article(document)
        source_hash = document[:document]._source
        event_value = source_hash['article']
        event_name = source_hash['label']
        link_name = "#{event_name} on Wikipedia"
        link_to link_name, event_value, target: '_blank'
    end

    def link_to_part_of(document)
        source_hash = document[:document]._source
        event_value = source_hash['part_of']
        #value of part of is an array, for every element call link_to_search
        event_value.map { |search_term| link_to_search(search_term) }.join(', ').html_safe
    end

    def link_to_search(search_term)
        base_url = 'http://127.0.0.1:3000/catalog/'
        search_path = '?search_field=part_of&q='
        exact_search_term = "\"" + search_term + "\""
    
        link_to(search_term, "#{base_url}#{search_path}#{CGI.escape(exact_search_term)}")
    end

    def link_to_page(document)
        base_url = 'http://127.0.0.1:3000/catalog/'
        id = document[:document].id
        link_to('Read More', "#{base_url}#{id}")
    end
        

    def link_to_coordinate_location(document)
        source_hash = document[:document]._source
        coordinate_location = source_hash['coordinate_location']
        parse_and_generate_map_link(coordinate_location)
    end

    def parse_and_generate_map_link(coordinate_location)
        coordinate_location = coordinate_location.to_s
        match_data = coordinate_location.match(/Point\((?<lat>[-+]?\d*\.\d+)\s(?<lng>[-+]?\d*\.\d+)\)/)
    
        if match_data
          lat = match_data[:lat]
          lng = match_data[:lng]
          link_to_map(lat, lng)
        else
          "Invalid coordinate location format"
        end
      end
    
    def link_to_map(lat, lng)
        link = "https://www.openstreetmap.org/?mlat=#{lat}&mlon=#{lng}#map=5/#{lat}/#{lng}"
        name_of_link = "#{lat}, #{lng}"
        link_to name_of_link, link, target: '_blank'
    end

    def is_catalog_page?
        if params[:controller] == 'catalog'
              true
            else
              false
         end
      end
end
