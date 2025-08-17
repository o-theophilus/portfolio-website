<script>
	import { onMount } from 'svelte';
	import { Content } from '$lib/layout';
	import { Button } from '$lib/button';

	let editor;

	onMount(async () => {
		if (typeof window !== 'undefined') {
			const EditorJS = (await import('@editorjs/editorjs')).default;
			const Header = (await import('@editorjs/header')).default;
			editor = new EditorJS({
				holder: 'editorjs',
				placeholder: 'Let`s write an awesome story!',
				inlineToolbar: ['header', 'bold', 'italic'],
				tools: {
					header: {
						class: Header,
						config: {
							placeholder: 'Enter a header',
							levels: [2, 3, 4],
							defaultLevel: 3
						}
					}
				}
			});
		}
	});
</script>

<Content>
	<Button onclick={() => editor.readOnly.toggle()}>Edit</Button>
	<div id="editorjs"></div>
</Content>
