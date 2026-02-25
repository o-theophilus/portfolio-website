<script>
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { Marked } from '$lib/macro';

	let post = module.value.post;
	let content = $state(post.content);
	let error = $state({});

	const validate = () => {
		error = {};

		if (!content) {
			error.content = 'This field is required';
		} else if (content == post.content) {
			error.content = 'No changes were made';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ content })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.post);
			module.close();
			notify.open('Content Saved');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Content" error={error.error}>
	<div class="marked">
		<Marked content={module.value.process({ ...post, content })} />
	</div>

	<IG
		name="Content"
		bind:value={content}
		error={error.content}
		type="textarea"
		placeholder="Content here"
		onkeydown={(e) => {
			if (e.key === 'Tab') {
				e.preventDefault();
				const start = e.target.selectionStart;
				const end = e.target.selectionEnd;

				const text = content;
				content = `${text.substring(0, start)}\t${text.substring(end)}`;

				e.target.selectionStart = e.target.selectionEnd = start + 1;
			}
		}}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
	.marked {
		overflow: auto;
		max-height: 300px;
		width: 100%;
		/* display: none; */
	}

	/* @media screen and (min-width: 700px) {
		.marked {
			display: block;
		}
		.marked {
			width: 100%;
		}
	}

	@media screen and (min-height: 600px) {
		.marked {
			display: block;
		}
	} */
</style>
