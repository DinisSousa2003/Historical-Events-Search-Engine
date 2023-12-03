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
        link_to event_value, event_value, target: '_blank'
    end
      
    def link_to_article(document)
        source_hash = document[:document]._source
        event_value = source_hash['article']
        link_to event_value, event_value, target: '_blank'
    end
end
