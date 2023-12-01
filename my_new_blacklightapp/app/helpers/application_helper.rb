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
end
