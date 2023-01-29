<script>
	export const prerender = true;

	import { template } from './template.js';
	import Input from '$lib/comp/input_group.svelte';
	import Button from '$lib/comp/button.svelte';

	import Sending from './sending.svelte';

	let form = {};
	let error = {};

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'cannot be empty';
		}

		if (!form.email) {
			error.email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'invalid entry';
		}

		if (!form.message) {
			error.message = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	let state = 0;
	const submit = async () => {
		state = 1;
		const resp = await fetch('https://formspree.io/f/xknkjbpb', {
			method: 'post',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(form)
		});

		const data = await resp.json();

		if (resp.ok) {
			state = 2;
		} else {
			state = 0;
			error.form = data.error;
		}
	};

	let msgStore = '';
</script>

<div class="form_position">
	{#if state > 0}
		<Sending
			{state}
			on:closed={() => {
				state = 0;
				form = {};
			}}
		/>
	{/if}

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<Input name="full name" error={error.name} let:id svg="username">
			<input placeholder="Your Name" type="text" {id} bind:value={form.name} />
		</Input>

		<Input name="email address" error={error.email} let:id svg="emailAddress">
			<input placeholder="Your Email Address" type="text" {id} bind:value={form.email} />
		</Input>
		<Input name="message" error={error.message} let:id>
			<svelte:fragment slot="label">
				<select name="template" id="" bind:value={form.message}>
					<option value={msgStore}>Message</option>
					{#each template as temp}
						<option value={temp.text}>{temp.name}</option>
					{/each}
				</select>
			</svelte:fragment>

			<textarea
				placeholder="Your Message"
				{id}
				bind:value={form.message}
				on:input={() => (msgStore = form.message)}
			/>
		</Input>
		{#if error.form}
			<div class="err">
				{error.form}
			</div>
		{/if}
		<Button class="wide">Send</Button>
	</form>
</div>

<style>
	.form_position {
		position: relative;
	}
</style>
