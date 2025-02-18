

function speechApp() {
    return {
        text: '',
        selectedLanguage: '',
        selectedModel: '',
        languages: [],
        models: [],
        status: '',
        audioFile: '',
        audioFiles: [],
        isGenerating: false,
        rate: 1.0,
        stats: {
            wordCount: 0
        },
        filename: '',

        async initialize() {
            await this.loadLanguages();
            this.$nextTick(async () => {
                if (this.languages?.length) {                    
                    this.selectedLanguage = 'us';
                    await this.loadModels();
                
                    if (this.models?.length) {
                        this.selectedModel = this.models[0]
                    }
                }
            })            
            await this.loadAudioFiles();
        },

        async loadLanguages() {
            try {
                const response = await fetch('/languages');
                const data = await response.json();
                this.languages = data.languages;
            } catch (error) {
                console.error('Error loading languages:', error);
            }
        },

        async loadModels() {
            if (!this.selectedLanguage) return;

            try {
                const response = await fetch(`/models/${this.selectedLanguage}`);
                const data = await response.json();
                this.models = data.models;
            } catch (error) {
                console.error('Error loading models:', error);
            }
        },

        async generateSpeech() {
            this.status = 'Generating speech...';
            this.isGenerating = true;

            try {
                const formData = new FormData(document.querySelector('form'))
                formData.append('rate', this.rate);  // Append rate value
                formData.append('name', this.filename);

                // Send the request to generate speech
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData,
                });

                const data = await response.json();
                await this.pollTaskStatus(data.task_id);
            } catch (error) {
                this.status = 'An error occurred.';
                this.isGenerating = false;
                console.error('Error generating speech:', error);
            }
        },

        async pollTaskStatus(taskId) {
            const checkStatus = async () => {
                try {
                    const response = await fetch(`/check_status/${taskId}`);
                    const data = await response.json();

                    if (data.status === 'completed') {
                        this.status = 'Speech generation completed!';
                        this.audioFile = data.audio_file;
                        this.isGenerating = false;
                    } else {
                        setTimeout(checkStatus, 3000);
                    }
                } catch (error) {
                    this.status = 'Failed to check status.';
                    this.isGenerating = false;
                    console.error('Error checking task status:', error);
                }
            };
            await checkStatus();
        },

        async loadAudioFiles() {
            try {
                this.audioFiles = [];
                const response = await fetch('/audio_files');
                const data = await response.json();
                this.audioFiles = data.audio_files;
            } catch (error) {
                console.error('Failed to load audio files:', error);
            }
        },

        humanizeFilename(filename) {
            return filename
                .replace(/-/g, ' ')          // Replace hyphens with spaces
                .replace(/\.wav$/, '')       // Remove the file extension
                .trim()                      // Remove any trailing spaces
                .replace(/\b\w/g, char => char.toUpperCase()); // Capitalize first letter of each word
        },

        clear(what) {
            switch (what) {
                case 'name':
                    this.filename = '';
                    break;
                case 'text':
                    this.text = '';
                    break;
                default:
                    console.warn(`Unknown field: ${field}`);
            }
        }
    };
}