import { Oval } from 'react-loader-spinner'
import './Loading.css'

export function Loading() {
  return (
    <div className="loading">
      <Oval
        height={48}
        width={48}
        color="var(--color-primary)"
        secondaryColor="var(--color-border)"
        strokeWidth={4}
        strokeWidthSecondary={4}
      />
    </div>
  )
}
