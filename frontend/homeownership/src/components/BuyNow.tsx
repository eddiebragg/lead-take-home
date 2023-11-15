import { FormEvent, useState } from "react"

export default function BuyNow({ propertyId, submitHandler } : { propertyId : string, submitHandler: any}) {
    const [error, setError] = useState<string | null>(null)
    const [success, setSuccess] = useState<string | null>(null)

    async function onSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault()
        setError(null)

        const formData = new FormData(event.currentTarget)
        const response = await fetch('http://127.0.0.1:8000/api/payment/', {
            method: 'POST',
            body: formData,
        })

        const data = await response.json()

        if (response.ok) {
            setSuccess("Payment successful! Your ownership share has increased accordingly.");
            submitHandler();
        } else {
            let message = '';

            if (data.amount) {
                message = data.amount[0]
            }

            if (data.non_field_errors) {
                message = data.non_field_errors[0]
            }
            setError(message);
        }



      }


    return (
        <form onSubmit={onSubmit} className="form">
            <p>I want to buy more of my home</p>
            
            <input type="hidden" name="property" value={propertyId} />
            <input type="number" name="amount" required />
            <button type="submit">Buy Now</button>
            {error && <p className="error">{error}</p>}
            {success && <p className="success">{success}</p>}
        </form>
       
    )
}