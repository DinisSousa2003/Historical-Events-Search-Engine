Rails.application.routes.draw do
  concern :range_searchable, BlacklightRangeLimit::Routes::RangeSearchable.new
  get 'static_pages/home'
  mount Blacklight::Engine => '/'
  concern :marc_viewable, Blacklight::Marc::Routes::MarcViewable.new
  
  #IF WE WANT TO HAD A STATIC PAGE, SWITCH FOR THIS
  root to: "static_pages#home"
  #root to: "catalog#index"
  concern :searchable, Blacklight::Routes::Searchable.new

  resource :catalog, only: [:index], as: 'catalog', path: '/catalog', controller: 'catalog' do
    concerns :searchable
    concerns :range_searchable

  end

  concern :exportable, Blacklight::Routes::Exportable.new

  resources :solr_documents, only: [:show], path: '/catalog', controller: 'catalog' do
    concerns [:exportable, :marc_viewable]
  end

  resources :bookmarks do
    concerns :exportable

    collection do
      delete 'clear'
    end
  end
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  get "up" => "rails/health#show", as: :rails_health_check

  get '/map', to: 'static_page_controller#map_action', as: :map

  # Defines the root path route ("/")
  # root "posts#index"
end
